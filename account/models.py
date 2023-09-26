from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(
            self, email, first_name, last_name, contact, password=None,
            commit=True):
        """
        Creates and saves a User with the given email, first name, last name
        and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not password:
            raise ValueError(_('Users must have a password'))
        if not first_name:
            raise ValueError(_('Users must have a first name'))
        if not last_name:
            raise ValueError(_('Users must have a last name'))
        if not contact:
            raise ValueError(_('Users must have a contact number'))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            contact=contact,
        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, contact, password):
        """
        Creates and saves a superuser with the given email, first name,
        last name and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            contact=contact,
            commit=False,
        )
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


sa_phone_regex = RegexValidator(
    regex=r'^(?:\+27|0)\d{9}$',
    message="Phone number must be a valid South African number in the format: '+27839133030' or '0839133030'."
)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact = models.CharField(validators=[sa_phone_regex], max_length=13)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'contact']

    def __str__(self):
        return self.email

    class Meta:
        ordering = ('-date_joined',)


# TODO:Password Reset

class EmailVerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(length=64)
        return super().save(*args, **kwargs)
