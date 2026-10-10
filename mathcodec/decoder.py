import json
import math
from pathlib import Path

from .checksum import sha256_bytes
from .models import MathCodecModel


def modular_inverse(
    value: int,
    modulus: int,
) -> int:

    if math.gcd(value, modulus) != 1:
        raise ValueError(
            "Multiplier has no modular inverse."
        )

    return pow(value, -1, modulus)


def decode_model(
    model: MathCodecModel,
) -> bytes:

    inverse = modular_inverse(
        model.multiplier,
        model.modulus,
    )

    decoded = [
        (
            inverse * (value - model.offset)
        ) % model.modulus
        for value in model.encoded_data
    ]

    data = bytes(decoded)

    if len(data) != model.original_size:
        raise ValueError(
            "Decoded size does not match original size."
        )

    calculated_hash = sha256_bytes(data)

    if calculated_hash != model.sha256:
        raise ValueError(
            "Integrity verification failed."
        )

    return data


def decode_file(
    input_path: str,
    output_path: str,
) -> Path:

    input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(input_path)

    raw = json.loads(
        input_file.read_text(
            encoding="utf-8"
        )
    )

    model = MathCodecModel.model_validate(raw)

    data = decode_model(model)

    output_file = Path(output_path)
    output_file.write_bytes(data)

    return output_file


def load_model(
    input_path: str,
) -> MathCodecModel:

    raw = json.loads(
        Path(input_path).read_text(
            encoding="utf-8"
        )
    )

    return MathCodecModel.model_validate(raw)