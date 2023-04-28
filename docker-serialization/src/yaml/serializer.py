from dataclasses import asdict
from typing import Any, Dict
import yaml

from ..interfaces import interfaces
from ..testing_data import data


class YamlSerializer(interfaces.Serializer):
    testing_data: Dict[str, Any]

    def prepare(self, testing_data: "data.TestingData"):
        self.testing_data = asdict(testing_data)

    def serialize(self) -> bytes:
        return yaml.dump(self.testing_data, Dumper=yaml.CSafeDumper)

    def deserialize(self, bts: bytes):
        _ = yaml.load(bts, Loader=yaml.CSafeLoader)


def make_serializer() -> interfaces.Serializer:
    return YamlSerializer()