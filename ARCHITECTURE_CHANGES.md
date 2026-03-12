## Uni-Learn – Recent Architectural Changes

This document explains the main design and business-logic changes that were introduced, and how they affect the way the system behaves.

---

## 1. Settings, secrets, and environment

- **What changed**
  - `uni_core/settings.py` no longer hardcodes `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, or Postgres credentials.
  - These values are now read from environment variables (see `.env.example`).
  - DRF throttling now has both `DEFAULT_THROTTLE_CLASSES` and `DEFAULT_THROTTLE_RATES` configured, so rate limits actually apply.
  - Test runs (`manage.py test`) automatically use a local SQLite database (by default) so you can run tests without PostgreSQL running.

- **Why**
  - Avoid committing secrets and prod-like settings into source control.
  - Make it explicit that API usage is throttled and avoid “it looks configured but does nothing”.
  - Make tests easy to run on any machine/CI environment.

---

## 2. Authentication and user signup

### 2.1 Public signup is always a student

- **What changed**
  - `UserSignUpSerializer` (in `authentication/serializers.py`) no longer exposes `role` as an input field.
  - The `create()` method always creates a `CustomUser` with:
    - The provided `username`, name, email, password.
    - `role="student"` (using your existing `ROLES` enum values).

- **Business rule**
  - *Public* registration can never create staff/admin accounts. Only students are created via `/api/auth/register/`.

- **Why**
  - Previously, a caller could pass `"role": "admin"` and become an admin immediately.
  - Staff accounts should be created through an admin-only path (admin site or dedicated staff endpoints).

### 2.2 JWT-related debug and decode endpoint

- **What changed**
  - Removed `print()` calls that were logging JWT payloads in `CustomTokenObtainPairSerializer` and `CustomTokenRefreshSerializer`.
  - `DecodeTokenView` now:
    - Requires `IsAdminUser`.
    - Returns a 404-style response when `DEBUG` is `False` (effectively disabled in production).

- **Business rule**
  - Token contents are treated as sensitive; you don’t log them in plain text or expose a “decode” endpoint to normal users.
  - Token decoding is a *debug/admin-only* diagnostic, and only when `DEBUG` is enabled.

---

## 3. Enrollment registration – new service layer

The biggest business-logic refactor is around how students register for courses.

### 3.1 Old design (before)

- Logic lived mainly inside `EnrollmentsRegistrationSerializer`:
  - It directly queried `Course` and `Enrollment`.
  - It enforced uniqueness (“already enrolled in this course”).
  - It created `Enrollment` records with a hardcoded `"Registered"` string for status.
- The view simply instantiated the serializer and returned `len(enrollments)` from the list returned by `serializer.save()`.
- Permissions on the endpoint allowed **anyone** to hit it (`AllowAny`), even anonymous callers.

**Problems**
- Business rules were spread across the serializer and view, not reusable anywhere else.
- Status string didn’t match the `EnrollmentStatus` choices.
- Endpoint was effectively unauthenticated, and assumed `request.user.student_profile`, which would fail for anonymous users.

### 3.2 New design (after)

#### 3.2.1 Dedicated domain service

- New file: `enrollments/services.py`
- Core function:

```python
def register_courses_for_student(*, student, course_ids: list[str]) -> EnrollmentResult:
    """
    Domain service for student course registration.
    Keeps business rules out of serializers/views.
    """
```

- **Business rules inside the service**
  - Reject duplicated course IDs (same course twice in one request).
  - Require that there is exactly one **open** semester (`Semester.objects.get(is_open=True)`).
  - Each course ID must:
    - Exist.
    - Belong to the current open semester.
  - A student cannot enroll in the same course twice (`Enrollment.objects.filter(student=student, course=course).exists()`).
  - All enrollments are created with `EnrollmentStatus.REGISTERED` (i.e. the enum constant, not a raw string).
  - All inserts happen inside a single `transaction.atomic()` block and use `bulk_create()` for performance.

- **Return type**
  - Returns an `EnrollmentResult` dataclass with `created_count`, so the API doesn’t need to know about the raw `Enrollment` list.

#### 3.2.2 Serializer becomes thin

- `EnrollmentsRegistrationSerializer` (in `enrollments/serializers.py`):
  - Still defines the payload shape: a `courses` list of IDs (as strings).
  - No longer contains core business rules; `validate()` only enforces structure, then `create()` calls the service:

```python
def create(self, validated_data):
    student = self.context["request"].user.student_profile
    course_ids = validated_data["courses"]
    result = register_courses_for_student(student=student, course_ids=course_ids)
    return result
```

- This keeps serializers focused on:
  - Input shape (what the API accepts).
  - Handing off to domain logic (what the system does).

#### 3.2.3 View handles permissions and response

- `EnrollmentRegistrationView` (in `enrollments/views.py`):
  - `permission_classes = [IsAuthenticated, IsStudent]` — only logged-in students can register.
  - On `POST`, it:
    - Instantiates the serializer with the request + context.
    - Calls `serializer.is_valid(raise_exception=True)`.
    - Calls `serializer.save()` → which returns `EnrollmentResult`.
    - Returns a response containing the `created_count`.

- **Business rules at the view layer**
  - “Only students can hit this endpoint” is enforced by DRF permissions.
  - Actual registration rules are centralized in the service, not duplicated across views.

---

## 4. Semester and enrollment integrity

### 4.1 Single open semester invariant

- **What changed**
  - `Semester` (in `academics/models.py`) now has:
    - A `Meta.constraints` entry with a `UniqueConstraint` on `is_open` with `condition=Q(is_open=True)` to ensure only one row can have `is_open=True`.
    - A corrected `clean()` method:
      - Still validates `end_date > start_date`.
      - When `is_open` is `True`, it checks for any other `Semester` with `is_open=True` and a different primary key, and raises a `ValidationError` if found.
    - Removed leftover debug `print()` and unused imports.

- **Business rule**
  - At any point in time, there can be at most **one** open semester.
  - This rule is enforced at both:
    - The application level (`clean()`).
    - The database level (unique constraint).

### 4.2 Enrollment marks bounds

- **What changed**
  - `Enrollment` (in `enrollments/models.py`) now adds validators:
    - `practical_mark`: `0.0`–`50.0`.
    - `theoretical_mark`: `0.0`–`50.0`.

- **Business rule**
  - Marks for a single course are bounded; invalid marks (negative or >50 per component) are rejected at the model/DB validation layer.
  - `is_passed` still checks `practical_mark + theoretical_mark >= 50`, but with sane bounds now guaranteed.

---

## 5. DRF configuration and tests

### 5.1 DRF settings

- **Changes**
  - `REST_FRAMEWORK` now includes:
    - `DEFAULT_THROTTLE_CLASSES` with `AnonRateThrottle` and `UserRateThrottle`.
    - The existing `DEFAULT_THROTTLE_RATES` you already had.
  - This ensures throttling applies globally, as originally intended.

### 5.2 Regression tests

- `authentication/tests.py`
  - Verifies that hitting `/api/auth/register/` with `"role": "admin"` still results in a user whose role is `student`.

- `enrollments/tests.py`
  - Verifies that `/api/semesters/current/register` cannot be called successfully by an anonymous client (ensures auth is required).

- These tests act as **guards** so future refactors do not accidentally reintroduce the most critical issues (role escalation, open enrollment to anonymous clients).

---

## 6. Student vs staff creation endpoints

- **Current state**
  - There is a **single public registration endpoint**: `/api/auth/register/`.
  - This endpoint:
    - Always creates a `CustomUser` with `role="student"`.
    - Does **not** create a corresponding `Student` profile record yet (that would be a separate concern to wire up).
  - There are **no dedicated API endpoints** for creating:
    - Employees.
    - Teachers / teaching assistants.
    - Admins.
  - Staff and admins should currently be created via the Django admin or via future, restricted endpoints.

- **Recommended design (future work)**
  - Add admin-only endpoints (or views) for staff creation, for example:
    - `/api/staff/teachers/` – admin-only; creates a `CustomUser` with `role="teacher"` (and any `Teacher` profile if needed).
    - `/api/staff/employees/` – admin-only; creates `role="employee"`.
  - Permissions:
    - Use `IsAdminUser` or a custom permission based on `user.is_admin`.
  - Business rule:
    - All non-student roles are created **only** through admin-controlled flows, never public registration.

This separation keeps the public API safe while still allowing you to extend staff-management in a controlled, explicit way.

