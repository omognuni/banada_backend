from enum import Enum


class Choices(str, Enum):
    @classmethod
    def choices(cls):
        return tuple((x.value, x.name) for x in cls)

    @classmethod
    def values(cls):
        return (x.value for x in cls)

    def __str__(self):
        return self.value
