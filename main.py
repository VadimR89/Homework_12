from collections import UserDict
import pickle
import os


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not self.validate_phone():
            raise ValueError("Invalid phone number format")

    def validate_phone(self):
        return len(self.value) == 10 and self.value.isdigit()


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)

    def remove_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                self.phones.remove(phone_obj)

    def edit_phone(self, old_phone, new_phone):
        found = False
        for phone_obj in self.phones:
            if phone_obj.value == old_phone:
                phone_obj.value = new_phone
                found = True
        if not found:
            raise ValueError(f"Phone number '{old_phone}' not found in the record")

    def find_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj


class AddressBook(UserDict):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.load_from_disk()  # Завантажуємо дані з диска при створенні
        if not os.path.exists(self.filename):
            with open(self.filename, 'wb') as file:
                pickle.dump({}, file)

    def save_to_disk(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_disk(self):
        try:
            with open(self.filename, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record
        self.save_to_disk()

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            self.save_to_disk()

    def find(self, query):
        results = []
        for name, record in self.data.items():
            if query in name or any(query in phone.value for phone in record.phones):
                results.append(record)
        return results


book = AddressBook('address_book.txt')


