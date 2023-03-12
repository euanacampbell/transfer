from datetime import datetime, timedelta
from dateutil import parser


def get_expiry(expiry_option):

    # Incorrect value provided
    options = ['0.5', '1', '10', '30', '60']
    if expiry_option not in options:
        raise Exception(f'Expiry option "{expiry_option}" not allowed.')

    # Create time delay
    expiry_time = datetime.now() + timedelta(minutes=float(expiry_option))

    return expiry_time


def date_to_string(date):

    return str(date)


def string_to_date(strtime):

    return parser.parse(strtime)


def format_expiry(date_as_string):

    if not date_as_string:
        return False

    expiry = string_to_date(date_as_string)

    formatted_date = datetime.strftime(
        expiry, "%d/%b/%Y %H:%M:%S")

    return formatted_date


def time_left(date_as_string):

    if not date_as_string:
        return False

    now = datetime.now()
    expiry = string_to_date(date_as_string)
    time_left = expiry-now

    return str(time_left)[:7]
