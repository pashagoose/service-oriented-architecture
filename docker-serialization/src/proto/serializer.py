from typing import List, Optional

from ..interfaces import interfaces
from .user_pb2 import User, Friend, TestingData
from ..testing_data import data


class ProtoSerializer(interfaces.Serializer):
    testing_data: Optional[TestingData]

    def prepare(self, testing_data: "data.TestingData"):
        self.testing_data = TestingData(
            users=[
                User(
                    name=user.name,
                    id=user.id,
                    friends=[Friend(id=friend.id, money=friend.money, name=friend.name) for friend in user.friends], 
                    cars=user.cars
                ) for user in testing_data.users
            ]
        )

    def serialize(self) -> bytes:
        return self.testing_data.SerializeToString()

    def deserialize(self, bts: bytes):
        message = TestingData()
        message.ParseFromString(bts)


def make_serializer() -> interfaces.Serializer:
    return ProtoSerializer()