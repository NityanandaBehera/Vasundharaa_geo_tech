from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

class Organization(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    def get_users(self):
        """Returns all users belonging to this organization."""
        return self.users.all()

class Role(models.Model):
    name = models.CharField(max_length=50)  # e.g., Admin, Editor, Viewer

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)

        if 'organization' not in extra_fields or not extra_fields['organization']:
            # Automatically assign to the default organization if not provided
            extra_fields['organization'], _ = Organization.objects.get_or_create(
                name="Admin Organization", defaults={"is_main": True}   
            )

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='users', null=False
    )
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.organization.name})"
