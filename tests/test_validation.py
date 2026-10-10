
import pytest
from pydantic import ValidationError

from mathcodec.encoder import encode_bytes
from mathcodec.decoder import decode_model
from mathcodec.models import MathCodecModel


def test_rejects_non_invertible_multiplier():
    with pytest.raises(ValueError):
        encode_bytes(b"hello", multiplier=2, offset=0)


def test_rejects_invalid_multiplier_in_model():
    model = encode_bytes(b"hello").model_dump()
    model["multiplier"] = 2

    with pytest.raises(ValidationError):
        MathCodecModel.model_validate(model)


def test_rejects_out_of_range_encoded_byte():
    model = encode_bytes(b"hello").model_dump()
    model["encoded_data"][0] = 256

    with pytest.raises(ValidationError):
        MathCodecModel.model_validate(model)


def test_rejects_negative_original_size():
    model = encode_bytes(b"hello").model_dump()
    model["original_size"] = -1

    with pytest.raises(ValidationError):
        MathCodecModel.model_validate(model)


def test_rejects_wrong_encoded_size():
    model = encode_bytes(b"hello").model_dump()
    model["encoded_data"].pop()

    with pytest.raises(ValidationError):
        MathCodecModel.model_validate(model)


def test_rejects_malformed_checksum():
    model = encode_bytes(b"hello").model_dump()
    model["sha256"] = "invalid"

    with pytest.raises(ValidationError):
        MathCodecModel.model_validate(model)


def test_rejects_unknown_fields():
    model = encode_bytes(b"hello").model_dump()
    model["unexpected"] = True

    with pytest.raises(ValidationError):
        MathCodecModel.model_validate(model)


def test_detects_corrupted_data():
    model = encode_bytes(b"hello")
    corrupted = model.model_copy(
        update={"encoded_data": [0] * model.original_size}
    )

    with pytest.raises(
        ValueError,
        match="Integrity verification failed",
    ):
        decode_model(corrupted)
