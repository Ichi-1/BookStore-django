import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def email_validation(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_('You must provide a valid email'))

    def create_superuser(self, email, name, password, **other_fields):

        if email:
            email = self.normalize_email(email)
            self.email_validation(email)
        else:
            raise ValueError(_('Superuser Account: You must provide a email'))

        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True")
        return self.create_user(email, name, password, **other_fields)

    def create_user(self, email, name, password, **other_fields):
        if email:
            email = self.normalize_email(email)
            self.email_validation(email)
        else:
            raise ValueError(_('Customer Account: You must provide a email'))

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(max_length=150)
    mobile = models.CharField(max_length=150, blank=True)
    # User Status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(
            subject=subject,
            message=message,
            from_email="admin@admin.com",
            recipient_list=[self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.name


class Address(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    customer = models.ForeignKey(
        Customer,
        verbose_name=_('Customer'),
        on_delete=models.CASCADE
    )
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    postcode = models.CharField(max_length=50)
    address_line = models.CharField(_('Address Line 1'), max_length=255)
    address_line2 = models.CharField(_('Address Line 2'), max_length=255)
    town_city = models.CharField(_('Town/City/State'), max_length=150)
    delivery_instructions = models.CharField(_('Delivery Instructions'), max_length=255)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    default = models.BooleanField(_('Default'), default=False)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'{self.full_name} Address'
