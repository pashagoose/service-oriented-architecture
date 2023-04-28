from abc import abstractmethod, ABCMeta
from typing import List

from ..testing_data import data

class Serializer(metaclass=ABCMeta):
    @abstractmethod
    def prepare(self, users: List["data.User"]):
        return

    @abstractmethod
    def serialize(self) -> bytes:
        return

    @abstractmethod
    def deserialize(self, bts: bytes):
        return