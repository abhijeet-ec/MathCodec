
import argparse
import sys

from mathcodec.decoder import decode_file, decode_model, load_model
from mathcodec.encoder import encode_file


def cmd_encode(args):
    output = encode_file(args.input, args.output)
    print("Encoded successfully")
    print(f"Output: {output}")


def cmd_decode(args):
    output = decode_file(args.input, args.output)
    print("Decoded and integrity-verified successfully")
    print(f"Output: {output}")


def cmd_verify(args):
    model = load_model(args.input)
    data = decode_model(model)

    print("MathCodec file verified successfully")
    print(f"Format: {model.format} v{model.version}")
    print(f"Decoded size: {len(data)} bytes")
    print(f"SHA-256: {model.sha256}")


def cmd_info(args):
    model = load_model(args.input)

    print("MathCodec Representation")
    print("=" * 45)
    print(f"ID:             {model.id}")
    print(f"Version:        {model.version}")
    print(f"Type:           {model.data_type}")
    print(f"Original size:  {model.original_size} bytes")
    print(f"Method:         {model.method}")
    print(f"Equation:       {model.equation}")
    print(f"Multiplier:     {model.multiplier}")
    print(f"Offset:         {model.offset}")
    print(f"Modulus:        {model.modulus}")
    print(f"SHA-256:        {model.sha256}")
    print(f"Encoded values: {len(model.encoded_data)}")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="mathcodec",
        description="Reversible mathematical data representation system.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    encode = commands.add_parser("encode", help="Encode a file.")
    encode.add_argument("input")
    encode.add_argument("-o", "--output")
    encode.set_defaults(func=cmd_encode)

    decode = commands.add_parser("decode", help="Decode and verify a file.")
    decode.add_argument("input")
    decode.add_argument("-o", "--output", required=True)
    decode.set_defaults(func=cmd_decode)

    verify = commands.add_parser("verify", help="Verify a MathCodec file.")
    verify.add_argument("input")
    verify.set_defaults(func=cmd_verify)

    info = commands.add_parser("info", help="Inspect a MathCodec file.")
    info.add_argument("input")
    info.set_defaults(func=cmd_info)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        args.func(args)
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
