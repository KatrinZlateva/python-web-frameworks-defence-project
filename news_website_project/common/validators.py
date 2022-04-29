from datetime import date

from django.core.exceptions import ValidationError


class MaxFileSizeInMbValidator:
    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, value):
        filesize = value.file.size
        if filesize > self.max_size * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" % str(self.max_size))


def validate_year(value):
    year = value.year
    current_year = date.today().year
    if year < 1920 or year > int(current_year):
        raise ValidationError(f'Year must be between 1920 and {current_year}.')


def validate_only_characters(value):
    for ch in value:
        if not ch.isalpha():
            raise ValidationError('The name must contain only letters.')
