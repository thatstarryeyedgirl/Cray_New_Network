from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from cloudinary.models import CloudinaryField


class ChiefEditorManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, profile_picture=None):
        if not email:
            raise ValueError("Users must provide an email address")
        if not first_name:
            raise ValueError("Users must provide a first name")
        if not last_name:
            raise ValueError("Users must provide a last name")
        if not profile_picture:
            raise ValueError("Users must upload a profile picture")
        if not password:
            raise ValueError("Users must set a password")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            profile_picture=profile_picture
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, profile_picture=None):
        user = self.create_user(email, first_name, last_name, password, profile_picture)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    
class ChiefEditor(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_picture = CloudinaryField('image')
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = ChiefEditorManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "profile_picture"]

    def __str__(self):
        return self.email
    
    
