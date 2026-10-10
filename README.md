
# MathCodec

**A reversible mathematical data representation system.**

MathCodec transforms binary data using mathematical models and reconstructs the original bytes through an inverse operation.

## Core Principle

For every supported input `X`:

`Decode(Encode(X)) = X`

The current implementation uses a modular affine transformation:

`y = (a × x + b) mod 256`

The multiplier `a` must be coprime with 256 so that a modular inverse exists.

## Current Features

- Reversible binary encoding and decoding
- Modular affine mathematical model
- SHA-256 integrity verification
- JSON-based model serialization
- Command-line interface
- FastAPI backend
- Property-based and validation tests

## Important Limitations

MathCodec currently performs mathematical data representation, **not compression or encryption**. Its JSON representation may be larger than the original file.

## Requirements

- Python 3.13 or compatible Python version
- pip
- Node.js and npm for frontend development

## Installation

Clone the repository and enter the project directory:

```bash
git clone https://github.com/abhijeet-ec/MathCodec.git
cd MathCodec
```

Create and activate a virtual environment.

Linux with Bash:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Linux with Fish:

```fish
python3 -m venv .venv
source .venv/bin/activate.fish
```

Install Python dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run Tests

```bash
python -m pytest -v
```

## Run the API

```bash
uvicorn api.server:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore the API.

## Project Structure

```text
MathCodec/
├── api/
├── examples/
├── frontend/
├── mathcodec/
├── tests/
├── main.py
├── requirements.txt
└── README.md
```

## Roadmap

- Strengthen validation and error handling
- Define a versioned `.mx` file format
- Add more reversible mathematical models
- Benchmark size overhead and processing speed
- Investigate compression separately
- Complete the frontend
- Add continuous integration and release documentation

## Status

Early development — APIs, file formats, and features may change.

## License

No license has been selected yet.
