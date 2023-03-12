import dbm
from datetime import datetime

from modules.helper_functions import string_to_date, date_to_string, format_expiry, time_left


class Code:

    def __init__(self, code):
        self.code = code
        self.just_expired = False
        self.keys = self.get_keys()
        self.data = self.get_data()
        self.clipboard = self.data['clipboard'] or ''
        self.expiry = format_expiry(self.data['expiry']) or ''
        self.time_left = time_left(self.data['expiry']) or ''
        self.expired = self.has_expired()

        print(self.time_left)

        if self.expired:
            self.keys = None
            self.clipboard = None

    def get_keys(self):

        with dbm.open('db_store', 'c') as db:
            keys_found = []
            for key in db.keys():
                key_string = key.decode("utf-8")
                if key_string.startswith(self.code + "_"):
                    keys_found.append(key)

        return keys_found

    def get_data(self):

        found = {
            'clipboard': '',
            'expiry': ''
        }

        with dbm.open('db_store', 'c') as db:
            for key in self.keys:
                key_string = key.decode("utf-8").split('_')[1]
                found[key_string] = db[key].decode("utf-8")

        return found

    def set_key_pair(self, key, value):

        actual_key = f"{self.code}_{key}"

        with dbm.open('db_store', 'c') as db:
            db[actual_key] = value

        return True

    def add(self, data):
        """Add data in bulk for a key, all items of the dict must be strings"""

        for key in data:
            self.set_key_pair(key, data[key])

        return True

    def get_value(self, key):
        """Add data in bulk for a key, all items of the dict must be strings"""

        if key in self.data:
            return self.data[key]
        else:
            return None

    def has_expired(self):

        expiry = self.get_value('expiry')

        if not expiry:
            return True
        elif string_to_date(expiry) > datetime.now():
            return False
        else:
            self.set_key_pair('clipboard', '')
            self.set_key_pair('expiry', '')
            self.just_expired = True
            return True
