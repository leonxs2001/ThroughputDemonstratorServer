from enum import Enum


class DataUnit(Enum):
    GB = "GB", 1024 ** 3
    MB = "MB", 1024 ** 2
    KB = "KB", 1024
    B = "B", 1

    @classmethod
    def from_string(cls, value: str):
        for member in cls:
            if member.value[0] == value.upper():
                return member
        raise ValueError(f"{value} is not a valid {cls.__name__}")

class SendingType(Enum):
    FILE = "file"
    DUMMY = "dummy"

    @classmethod
    def from_string(cls, value: str):
        last_member = None
        for member in cls:
            if member.value == value.lower():
                return member
            last_member = member
        return last_member
