from dataclasses import asdict
import msgpack
from typing import Any, Dict

from ..interfaces import interfaces
from ..testing_data import data


class MsgPackSerializer(interfaces.Serializer):
    testing_data: Dict[str, Any]

    def prepare(self, testing_data: "data.TestingData"):
        self.testing_data = asdict(testing_data)

    def serialize(self) -> bytes:
        return msgpack.dumps(self.testing_data)

    def deserialize(self, bts: bytes):
        _ = msgpack.loads(bts)


def make_serializer() -> interfaces.Serializer:
    return MsgPackSerializer()