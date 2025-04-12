import falcon
import json

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import ed25519
from datetime import datetime, date


def json_serialize(obj):
    if isinstance(obj, datetime):
        return obj.astimezone().isoformat()
    elif isinstance(obj, date):
        return obj.astimezone().isoformat()
    else:
        return str(obj, encoding="utf-8")


def validate_payload(public_key: bytes, req):
    _public_key = ed25519.Ed25519PublicKey().from_public_bytes(public_key)
    signature_head = req.get_header(
        "x-measurement-signature",
        required=True,
        default="x-measurement-signature is missing",
    )
    alg, hex_signature = signature_head.split(":")
    if alg != "ed25519":
        raise falcon.HTTPBadRequest(
            title="Wrong signature algorithm",
            description="Wrong signature algorithm use. Use ed25519",
        )
    try:
        signature = bytes.fromhex(hex_signature)
    except ValueError:
        raise falcon.HTTPBadRequest(
            title="Invalid Signature", description="X-Measurement-Signature invalid"
        )
    with req.bounded_stream as rs:
        raw_body = rs.read()
    try:
        _public_key.verify(
            signature,
            raw_body,
        )
    except InvalidSignature:
        raise falcon.HTTPBadRequest(
            title="Invalid Signature",
            description="Provided signature does not match content",
        )

    return json.loads(raw_body)
