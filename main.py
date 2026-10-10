import argparse
import sys

from mathcodec.decoder import decode_file, load_model
from mathcodec.encoder import encode_file


def cmd_encode(args):
    output = encode_file(args.input, args.output)

    print("✓ Encoded successfully")
    print(f"Output: {output}")


def cmd_decode(args):
    output = decode_file(args.input, args.output)

    print("✓ Decoded successfully")
    print(f"Output: {output}")


def cmd_info(args):
    model = load_model(args.input)

    print()
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
    print()


def build_parser():

    parser = argparse.ArgumentParser(
        prog="mathcodec",
        description="Reversible mathematical data representation system.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    encode = subparsers.add_parser(
        "encode",
        help="Encode a file.",
    )

    encode.add_argument(
        "input",
        help="Input file.",
    )

    encode.add_argument(
        "-o",
        "--output",
        help="Output .mx file.",
    )

    encode.set_defaults(func=cmd_encode)

    decode = subparsers.add_parser(
        "decode",
        help="Decode a MathCodec file.",
    )

    decode.add_argument(
        "input",
        help="Input .mx file.",
    )

    decode.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output file.",
    )

    decode.set_defaults(func=cmd_decode)

    info = subparsers.add_parser(
        "info",
        help="Show mathematical representation.",
    )

    info.add_argument(
        "input",
        help="MathCodec .mx file.",
    )

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