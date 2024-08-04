import uuid
import pghistory

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import validate_email
from django.db import models

from common.abstract_models import AbstractExternalFacing, AbstractTimeStamped, AbstractVersioned
from common.constants import Length


class PlatformUserManager(BaseUserManager):
    def create_user(self, external_id: uuid.UUID, email: str, password: str = None) -> "PlatformUser":
        """
        Creates and saves a User with the given phone, and password.
        """
        validate_email(email)
        user = self.model(external_id=external_id, email=email)

        password = password or self.make_random_password()

        user.set_password(password)
        # JWT secret
        user.auth_secret = self.make_random_password(length=self.model.CONST_AUTH_SECRET_LEN)
        user.save(using=self._db)
        return user

    def create_superuser(self, external_id: uuid.UUID, email: str, password: str):  # pragma: no cover
        """
        Creates and saves a superuser with the given email, password.
        """
        user = self.create_user(external_id=external_id, email=email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


@pghistory.track()
class PlatformUser(AbstractBaseUser, AbstractExternalFacing, AbstractTimeStamped, AbstractVersioned):
    CONST_AUTH_SECRET_LEN = 16

    email = models.EmailField(blank=False, null=False, unique=True)
    phone = models.CharField(max_length=Length.PHONE_NUMBER, blank=True, null=True, unique=True)
    auth_secret = models.CharField(max_length=CONST_AUTH_SECRET_LEN, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    is_suspended = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = PlatformUserManager()

    USERNAME_FIELD = "external_id"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):  # pragma: no cover
        return self.email

    # TODO: What is the use of these methods ?
    def has_perm(self, perm, obj=None):  # pragma: no cover
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):  # pragma: no cover
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):  # pragma: no cover
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin
