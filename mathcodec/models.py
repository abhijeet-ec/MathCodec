
import math
import re
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


class MathCodecModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    format: Literal["MathCodec"] = "MathCodec"
    version: str = "0.1"

    id: str = Field(min_length=1)
    data_type: Literal["binary"]
    original_size: int = Field(ge=0)

    method: Literal["modular_affine"] = "modular_affine"

    modulus: Literal[256] = 256
    multiplier: int = Field(ge=1, le=255)
    offset: int = Field(ge=0, le=255)

    encoded_data: list[int]
    sha256: str

    @field_validator("multiplier")
    @classmethod
    def validate_multiplier(cls, value: int) -> int:
        if math.gcd(value, 256) != 1:
            raise ValueError(
                "Multiplier must be coprime with 256."
            )
        return value

    @field_validator("encoded_data")
    @classmethod
    def validate_encoded_data(
        cls,
        values: list[int],
    ) -> list[int]:
        if any(
            type(value) is not int or not 0 <= value <= 255
            for value in values
        ):
            raise ValueError(
                "Encoded values must be integers from 0 to 255."
            )
        return values

    @field_validator("sha256")
    @classmethod
    def validate_sha256(cls, value: str) -> str:
        if re.fullmatch(r"[0-9a-f]{64}", value) is None:
            raise ValueError(
                "SHA-256 must contain exactly 64 lowercase "
                "hexadecimal characters."
            )
        return value

    @model_validator(mode="after")
    def validate_size(self):
        if len(self.encoded_data) != self.original_size:
            raise ValueError(
                "Encoded data length must match original_size."
            )
        return self

    @property
    def equation(self) -> str:
        return (
            f"y = ({self.multiplier}x + "
            f"{self.offset}) mod {self.modulus}"
        )
