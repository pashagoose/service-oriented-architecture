from typing import List, Optional

from ..interfaces import interfaces
from .user import User, Friend, TestingData
from ..testing_data import data


class ProtoSerializer(interfaces.Serializer):
    testing_data: Optional[TestingData]

    def prepare(self, users: List["data.User"]):
        self.testing_data = TestingData(
            users=[
                User(
                    name=user.name,
                    id=user.id,
                    friends=[Friend(friend.id, friend.money, friend.name) for friend in user.friends], 
                    cars=user.cars
                ) for user in users
            ]
        )


    def serialize(self) -> bytes:
        return self.testing_data.SerializeToString()


    def deserialize(self, bts: bytes):
        message = TestingData()
        message.parse(data=bts)


def make_serializer() -> interfaces.Serializer:
    return ProtoSerializer()