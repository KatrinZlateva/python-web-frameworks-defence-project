import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

from news_website_project.accounts.managers import NewsUserManager


class NewsUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        null=False,
        blank=False,
        unique=True,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    USERNAME_FIELD = 'email'

    objects = NewsUserManager()


class Profile(models.Model):
    FIRST_NAME_MAX_LEN = 30
    FIRST_NAME_MIN_LEN = 2
    LAST_NAME_MAX_LEN = 30
    LAST_NAME_MIN_LEN = 2

    MALE = 'Male'
    FEMALE = 'Female'
    DO_NOT_SHOW = 'Do not show'

    GENDERS = [(x, x) for x in (MALE, FEMALE, DO_NOT_SHOW)]

    MIN_DATE = datetime.date(1920, 1, 1)

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LEN,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LEN),
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LEN,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LEN),
        )
    )

    email = models.EmailField()

    gender = models.CharField(
        max_length=max([len(x) for x, _ in GENDERS]),
        choices=GENDERS,
        null=True,
        blank=True,
        default=DO_NOT_SHOW,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    picture = models.URLField(
        null=False,
        blank=False,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        NewsUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_name_len(self):
        return len(self.full_name)
