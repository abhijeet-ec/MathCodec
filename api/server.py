
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response

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
    try:
        data = await file.read()
        model = encode_bytes(data)

        result = model.model_dump()
        result["equation"] = model.equation
        result["filename"] = file.filename

        return JSONResponse(content=result)
    finally:
        await file.close()


@app.post("/decode")
def decode(model: MathCodecModel):
    try:
        data = decode_model(model)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    return Response(
        content=data,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": 'attachment; filename="decoded.bin"',
            "X-MathCodec-Verified": "true",
            "X-MathCodec-SHA256": model.sha256,
        },
    )
