from datetime import date

from django.core.exceptions import ValidationError


def validate_year(value):
    year = value.year
    current_year = date.today().year
    if year < 1920 or year > int(current_year):
        raise ValidationError(f'Year must be between 1920 and {current_year}.')
