from django.core.validators import RegexValidator


# helper regex
phone_number_regex = RegexValidator(
    regex=r'^\+?[1-9]\d{1,14}$',
    message="Enter a valid international phone number format (up to 15 digits, e.g. +14155552671)."
)