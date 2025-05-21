from fastapi import FastAPI, Body, WebSocket, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from services.stt_service import *
from starlette.responses import Response
import ffmpeg

app = FastAPI()

origins = [
    # разрешенные источники
    "*"
]

app.add_middleware(
    # сначапо все запрещаем    
    CORSMiddleware,
    # потом начинаем разрешать необходимое
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def convert_webm_to_wav():
    ffmpeg.input("buffer.webm")
    ffmpeg.output("buffer.wav")

@app.websocket("/api/ws")
async def websocket_endpoint(websocket : WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        resp = speach_to_text_func(data)
        print(f"message: {resp}")
        await websocket.send_text(resp)

@app.post("/api/audio")
async def audio_endpoint(audio : UploadFile):
    data = (await audio.read())
    with open("buffer.wav", "wb") as wb:
        wb.write(data)
    # # print(data)
    # with open("buffer.wav", "rb") as rb:
    #     data = rb.read()
    resp = speach_to_text_func1()
    print(f"message: {resp}")

@app.get("/api/health")
async def health():
    return Response(status_code = status.HTTP_200_OK, content="OK")