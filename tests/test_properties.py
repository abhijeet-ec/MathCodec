from hypothesis import given, strategies as st

from mathcodec.decoder import decode_model
from mathcodec.encoder import encode_bytes


@given(st.binary())
def test_encode_decode_is_lossless(data):
    model = encode_bytes(data)

    decoded = decode_model(model)

    assert decoded == data