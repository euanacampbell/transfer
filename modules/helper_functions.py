from datetime import datetime, timedelta
from dateutil import parser


def get_expiry(expiry_option):

    options = ['once', '1', '10', '30', '60']

    # Incorrect value provided
    if expiry_option not in options:
        raise Exception(f'Expiry option "{expiry_option}" not allowed.')

    # Handle once
    if expiry_option == 'once':
        return 'once'

    # Create time delay
    current_time = datetime.now()
    # days, seconds, then other fields.
    expiry_time = current_time + timedelta(minutes=int(expiry_option))

    return expiry_time


def date_to_string(date):

    return str(date)


def string_to_date(strtime):

    return parser.parse(strtime)
