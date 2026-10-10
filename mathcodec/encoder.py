import json
import math
import secrets
from pathlib import Path

from .checksum import sha256_bytes, short_hash
from .models import MathCodecModel


def generate_multiplier(modulus: int = 256) -> int:
    candidates = [
        value
        for value in range(1, modulus)
        if math.gcd(value, modulus) == 1
    ]

    return secrets.choice(candidates)


def encode_bytes(
    data: bytes,
    multiplier: int | None = None,
    offset: int | None = None,
) -> MathCodecModel:

    modulus = 256

    if multiplier is None:
        multiplier = generate_multiplier(modulus)

    if math.gcd(multiplier, modulus) != 1:
        raise ValueError(
            "Multiplier must be coprime with modulus."
        )

    if offset is None:
        offset = secrets.randbelow(modulus)

    encoded = [
        (multiplier * byte + offset) % modulus
        for byte in data
    ]

    identifier = f"MX-{short_hash(data).upper()}"

    return MathCodecModel(
        id=identifier,
        data_type="binary",
        original_size=len(data),
        multiplier=multiplier,
        offset=offset,
        encoded_data=encoded,
        sha256=sha256_bytes(data),
    )


def encode_file(
    input_path: str,
    output_path: str | None = None,
) -> Path:

    input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(input_path)

    data = input_file.read_bytes()

    model = encode_bytes(data)

    if output_path is None:
        output_path = str(
            input_file.with_suffix(
                input_file.suffix + ".mx"
            )
        )

    output_file = Path(output_path)

    output_file.write_text(
        json.dumps(
            model.model_dump(),
            indent=2,
        ),
        encoding="utf-8",
    )

    return output_file