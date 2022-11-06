import datetime

from django.core.validators import MaxValueValidator


def max_value_current_year(value):
    year = datetime.date.today().year
    message = f'Год не может быть больше текущего {year}'
    return MaxValueValidator(year, message)(value)
