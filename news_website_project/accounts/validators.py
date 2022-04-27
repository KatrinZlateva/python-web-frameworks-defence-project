from datetime import date

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class MinDateValidator:
    def __init__(self, min_date):
        self.min_date = min_date

    def __call__(self, value):
        if value < self.min_date:
            raise ValidationError(f'Date must be greater than {self.min_date}')


@deconstructible
class MaxDateValidator:
    def __init__(self, max_date):
        self.max_date = max_date

    def __call__(self, value):
        if self.max_date < value:
            raise ValidationError(f'Date must be earlier than {self.max_date}')


def validate_year(value):
    year = value.year
    current_year = date.today().year
    if year < 1920 or year > int(current_year):
        raise ValidationError(f'Year must be between 1920 and {current_year}.')
