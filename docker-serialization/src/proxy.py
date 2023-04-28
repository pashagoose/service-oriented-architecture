from flask import Flask, request
import os
import requests


def _create_proxy_app():
    app = Flask(__name__)

    format_to_url = {}
    if os.environ.get("PROTO_HOST") is not None:
        format_to_url["proto"] = os.environ["PROTO_HOST"]
    if os.environ.get("XML_HOST") is not None:
        format_to_url["xml"] = os.environ["XML_HOST"]
    if os.environ.get("JSON_HOST") is not None:
        format_to_url["json"] = os.environ["JSON_HOST"]
    if os.environ.get("PICKLE_HOST") is not None:
        format_to_url["pickle"] = os.environ["PICKLE_HOST"]
    if os.environ.get("MSGPACK_HOST") is not None:
        format_to_url["msgpack"] = os.environ["MSGPACK_HOST"]
    if os.environ.get("AVRO_HOST") is not None:
        format_to_url["avro"] = os.environ["AVRO_HOST"]
    if os.environ.get("YAML_HOST") is not None:
        format_to_url["yaml"] = os.environ["YAML_HOST"]

    @app.route("/get_result")
    def get_result():
        if request.args.get("format") is None:
            return "No format is specified in query attributes", 400
        
        if format_to_url.get(request.args["format"]) is None:
            return f"Serialization format {request.args['format']} is not supported", 404

        url = f"{format_to_url[request.args['format']]}/get_result"
        response = requests.get(url)
        return bytes.decode(response.content, "utf-8")
    
    return app


def _start_proxy():
    app = _create_proxy_app()
    app.run(host="0.0.0.0", port=os.environ["PORT"])


if __name__ == "__main__":
    _start_proxy()