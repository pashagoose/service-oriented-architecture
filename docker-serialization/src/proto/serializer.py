# from user import User, Friend
from typing import List

from ..interfaces import interfaces
from ..testing_data import data


class ProtoSerializer(interfaces.Serializer):
    def prepare(self, users: List["data.User"]):
        pass


    def serialize(self) -> bytes:
        return bytes()


    def deserialize(self, bts: bytes):
        pass


def make_serializer() -> interfaces.Serializer:
    return ProtoSerializer()