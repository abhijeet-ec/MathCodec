from pydantic import BaseModel


class MathCodecModel(BaseModel):
    format: str = "MathCodec"
    version: str = "0.1"

    id: str

    data_type: str
    original_size: int

    method: str = "modular_affine"

    modulus: int = 256
    multiplier: int
    offset: int

    encoded_data: list[int]

    sha256: str

    @property
    def equation(self) -> str:
        return (
            f"y = ({self.multiplier}x + "
            f"{self.offset}) mod {self.modulus}"
        )