from abc import ABC, abstractmethod
import re

TEST_EMAIL = 'user@example.com'
TEST_EMAIL_UPPER = 'User@Example.COM'
TEST_EMAIL_NO_AT = 'userexample.com'
TEST_EMAIL_MULTI_AT = 'user@@example.com'
TEST_EMAIL_NO_LOCAL = '@example.com'
TEST_EMAIL_NO_DOMAIN = 'user@'
TEST_EMAIL_NO_TLD = 'user@example'
TEST_EMAIL_SPACE = 'user @example.com'


class Email(ABC):
    @abstractmethod
    def __init__(self, address: str):
        print("Can't init this class!")

    def __str__(self):
        return self.address


class StandardEmail(Email):
    PATTERN = re.compile(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$')

    def __init__(self, address: str):
        if not isinstance(address, str):
            raise TypeError(f'Bad type for address: {type(address)}')
        if ' ' in address:
            raise ValueError(f'Spaces not allowed in {address=}')
        if address.count('@') != 1:
            raise ValueError(f'Address must contain exactly one "@" in {address=}')
        local, domain = address.split('@')
        if not local:
            raise ValueError(f'Local part cannot be empty in {address=}')
        if not domain:
            raise ValueError(f'Domain cannot be empty in {address=}')
        if not self.PATTERN.match(address):
            raise ValueError(f'{address=} is not a valid email address')
        self.address = address.lower()
