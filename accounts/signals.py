from django.conf import settings
from django.db import IntegrityError, transaction
from django.dispatch import receiver
from django.db.models.signals import post_save

from accounts.models import CustomUser, Student


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.is_student:
        obj = Student.objects.create(user=instance, university_number= instance.username)

