from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from mathcodec.decoder import decode_model
from mathcodec.encoder import encode_bytes
from mathcodec.models import MathCodecModel


app = FastAPI(
    title="MathCodec API",
    description="Reversible mathematical data representation API",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "name": "MathCodec",
        "version": "0.1.0",
        "status": "online",
    }


@app.post("/encode")
async def encode(file: UploadFile = File(...)):
    data = await file.read()

    model = encode_bytes(data)

    response = model.model_dump()
    response["equation"] = model.equation
    response["filename"] = file.filename

    return JSONResponse(content=response)


@app.post("/decode")
async def decode(model: MathCodecModel):
    data = decode_model(model)

    return {
        "size": len(data),
        "sha256": model.sha256,
        "verified": True,
    }