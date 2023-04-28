from dataclasses import asdict
import dict2xml
from typing import Any, Dict
import xml.etree.ElementTree as ET

from ..interfaces import interfaces
from ..testing_data import data


class XmlPickleSerializer(interfaces.Serializer):
    testing_data: Dict[str, Any]

    def prepare(self, testing_data: "data.TestingData"):
        self.testing_data = asdict(testing_data)

    def serialize(self) -> bytes:
        return dict2xml.dict2xml(self.testing_data, wrap="testing_data")

    def deserialize(self, bts: bytes):
        _ = ET.ElementTree(ET.fromstring(bts))


def make_serializer() -> interfaces.Serializer:
    return XmlPickleSerializer()