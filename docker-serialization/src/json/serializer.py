import json
from dataclasses import asdict
from typing import List, Any

from ..interfaces import interfaces
from ..testing_data import data

class JsonSeriliazer(interfaces.Serializer):
    testing_data: List[Any]

    def prepare(self, testing_data: "data.TestingData"):
        self.testing_data = [asdict(user) for user in testing_data.users]

    def serialize(self) -> bytes:
        return json.dumps(self.testing_data)

    def deserialize(self, bts: bytes):
        _ = json.loads(bts)


def make_serializer() -> interfaces.Serializer:
    return JsonSeriliazer()