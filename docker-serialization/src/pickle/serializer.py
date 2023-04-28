import pickle

from ..interfaces import interfaces
from ..testing_data import data


class PickleSerializer(interfaces.Serializer):
    testing_data: data.TestingData

    def prepare(self, testing_data: "data.TestingData"):
        self.testing_data = testing_data

    def serialize(self) -> bytes:
        return pickle.dumps(self.testing_data)

    def deserialize(self, bts: bytes):
        pickle.loads(bts)


def make_serializer() -> interfaces.Serializer:
    return PickleSerializer()