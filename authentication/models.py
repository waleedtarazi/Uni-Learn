from django.db import models

# Create your models here.
class PasswordReset(models.Model):
    email = models.EmailField(unique=True, blank=False)
    token = models.CharField(blank=False, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

