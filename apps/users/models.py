import uuid
from datetime import timedelta

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import CIEmailField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from utils.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(
        self, email, first_name, last_name, phone_number, password=None, save=True
    ):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )

        user.set_password(password)
        if save:
            user.save(using=self._db)
        return user

    def create_superuser(
        self, email, first_name, last_name, phone_number, password=None
    ):
        user = self.create_user(
            email, first_name, last_name, phone_number, password=password, save=False
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(PermissionsMixin, AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = CIEmailField(verbose_name=_("email address"), max_length=255, unique=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    phone_number = models.CharField(max_length=20)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number"]

    class Meta:
        ordering = ("-created_on",)

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class PasswordRestoreRequest(BaseModel):
    expiration_minutes = 60  # 1 hour

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = CIEmailField(max_length=255, unique=True)

    expiration_date = models.DateTimeField(null=True, blank=True)

    @property
    def is_expired(self):
        return self.expiration_date < timezone.now()

    def mark_expired(self):
        self.expiration_date = self.expiration_date - timedelta(self.expiration_minutes)
        self.save()

    def save(self, *args, **kwargs):
        if not self.expiration_date and self.expiration_minutes:
            self.expiration_date = timezone.now() + timedelta(
                minutes=self.expiration_minutes
            )

        return super().save(*args, **kwargs)
