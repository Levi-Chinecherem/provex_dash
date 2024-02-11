# accounts/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    job = models.CharField(max_length=100, null=True, blank=True)
    about_you = models.TextField(null=True, blank=True)

    # Make email unique and required
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    # Add related_name to avoid clashes with auth.User model
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="customuser_set",  # Added related_name
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="customuser_set",  # Added related_name
    )
