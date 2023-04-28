import avro.io
import avro.schema

from dataclasses import asdict
import io
from typing import List, Any, Optional

from ..interfaces import interfaces
from ..testing_data import data

schema = """
{
    "namespace": "avro",
    "type": "record",
    "name": "User",
    "fields": [
        {
            "name": "name",
            "type": "string"
        },
        {
            "name": "id",
            "type": "int"
        },
        {
            "name": "friends",
            "type": {
                "type": "array",
                "items": {
                    "type": "record",
                    "name": "Friend",
                    "namespace": "avro",
                    "fields": [
                        {
                            "name": "id",
                            "type": "int"
                        },
                        {
                            "name": "money",
                            "type": "float"
                        },
                        {
                            "name": "name",
                            "type": "string"
                        }
                    ]
                }
            }
        },
        {
            "name": "cars",
            "type": {
                "type": "array",
                "items": "string"
            }
        }
    ]
}
"""

class AvroSeriliazer(interfaces.Serializer):
    testing_data: List[Any]
    schema: Optional[avro.schema.Schema]

    def prepare(self, testing_data: "data.TestingData"):
        self.schema = avro.schema.parse(schema)
        self.testing_data = [asdict(user) for user in testing_data.users]

    def serialize(self) -> bytes:
        bytes_writer = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        writer = avro.io.DatumWriter(self.schema)
        for user in self.testing_data:
            writer.write(user, encoder)
        return bytes_writer.getvalue()

    def deserialize(self, bts: bytes):
        bytes_reader = io.BytesIO(bts)
        reader = avro.io.DatumReader(self.schema, self.schema)
        decoder = avro.io.BinaryDecoder(bytes_reader)
        try:
            while reader.read(decoder=decoder) is not None:
                pass
        except Exception:
            pass


def make_serializer() -> interfaces.Serializer:
    return AvroSeriliazer()