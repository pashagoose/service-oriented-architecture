import argparse
from dataclasses import dataclass
import datetime
from flask import Flask
import logging
import timeit

from .interfaces import interfaces
from .json import serializer as json_serializer
from .pickle import serializer as pickle_serializer
from .proto import serializer as proto_serializer
from .testing_data import data
from .xml import serializer as xml_serializer


def _build_parser():
    parser = argparse.ArgumentParser(description="Start serialization test server")
    parser.add_argument(
        "--mode",
        dest="mode",
        type=str,
        help="Serialization format - one of (\"proto\", \"json\", \"pickle\", \"xml\", \"avro\", \"yaml\", \"messagepack\")",
        default="proto",
    )
    parser.add_argument(
        "--port",
        dest="port",
        type=int,
        help="Port to start http server on",
        default=2001
    )
    parser.add_argument(
        "--iterations",
        dest="iterations",
        type=int,
        help="Iteration count for testing serialization",
        default=1000,
    )
    return parser


@dataclass
class SerializationFormatResults:
    name: str
    serialized_size: int = 0
    serialization_time: datetime.timedelta = 0
    deserialization_time: datetime.timedelta = 0


def make_serializer(mode: str) -> interfaces.Serializer:
    if mode == "proto":
        return proto_serializer.make_serializer()
    elif mode == "json":
        return json_serializer.make_serializer()
    elif mode == "pickle":
        return pickle_serializer.make_serializer()
    elif mode == "xml":
        return xml_serializer.make_serializer()
    else:
        raise Exception(f"Serialization mode {mode} is not supported")


def _run_serialization_benchmark(mode: str, iterations: int = 1000) -> SerializationFormatResults:
    users = data.get_test_data()
    logging.info("Generated test data")

    serializer = make_serializer(mode)
    serializer.prepare(users)
    logging.info("Prepared serializer for mode `%s`", mode)

    serialized_bytes = serializer.serialize()
    result = SerializationFormatResults(name=mode, serialized_size=len(serialized_bytes))

    result.serialization_time = datetime.timedelta(
        seconds=timeit.timeit(
            "serializer.serialize()",
            number=iterations,
            globals={
                "serializer": serializer,
            },
        ) / iterations,
    )
    logging.info("Measured serialization time")

    result.deserialization_time = datetime.timedelta(
        seconds=timeit.timeit(
            "serializer.deserialize(serialized_bytes)", 
            number=iterations, 
            globals={
                "serializer": serializer,
                "serialized_bytes": serialized_bytes
            },
        ) / iterations,
    )
    logging.info("Measured deserialization time")

    return result


def _create_app(result: SerializationFormatResults):
    app = Flask(__name__)

    @app.route("/get_result")
    def get_result():
        return f"{result.name}-{result.serialized_size}-{result.serialization_time.microseconds / 1000}ms-{result.deserialization_time.microseconds / 1000}ms"

    return app


def _main():
    parser = _build_parser()
    args = parser.parse_args()

    # Set logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    # Perform serialization/deserialization benchmark
    results = _run_serialization_benchmark(args.mode, args.iterations)

    # Run server on given port with format results
    app = _create_app(results)
    
    logging.info("Starting server on port %d", args.port)
    app.run(host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    _main()
