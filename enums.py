from enum import Enum


class DataUnit(Enum):
    GB = "GB", 1024 ** 3
    MB = "MB", 1024 ** 2
    KB = "KB", 1024
    B = "B", 1

    @classmethod
    def from_string(cls, value: str):
        first_member = None
        for member in cls:
            if member.value[0] == value.upper():
                return member
            elif not first_member:
                first_member = member
        return first_member


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


class CommunicationType(Enum):
    DOWNLOAD = "download"
    UPLOAD = "upload"

    @classmethod
    def from_string(cls, value: str):
        first_member = None
        for member in cls:
            if member.value == value.lower():
                return member
            elif not first_member:
                first_member = member
        return first_member
