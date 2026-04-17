import calendar
from datetime import date


def is_birthday_today(dob: date, today: date) -> bool:
    month, day = dob.month, dob.day
    if month == 2 and day == 29 and not calendar.isleap(today.year):
        month, day = 2, 28
    return today.month == month and today.day == day
