from mathcodec.decoder import decode_model
from mathcodec.encoder import encode_bytes


def test_text_round_trip():
    original = b"Hello MathCodec!"

    model = encode_bytes(original)
    decoded = decode_model(model)

    assert decoded == original


def test_empty_data():
    original = b""

    model = encode_bytes(original)
    decoded = decode_model(model)

    assert decoded == original


def test_all_bytes():
    original = bytes(range(256))

    model = encode_bytes(original)
    decoded = decode_model(model)

    assert decoded == original


def test_large_data():
    original = bytes(range(256)) * 100

    model = encode_bytes(original)
    decoded = decode_model(model)

    assert decoded == original