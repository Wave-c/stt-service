from fastapi import FastAPI, Body, WebSocket, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from services.stt_service import *
from starlette.responses import Response
from moviepy import *

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

def convert_webm_to_wav(data:bytes):
    clip = DataVideoClip(data)
    clip.write_audiofile("buffer.wav", codec='wav')

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
    # print(data)
    resp = speach_to_text_func(data)
    print(f"message: {resp}")

@app.get("/api/health")
async def health():
    return Response(status_code = status.HTTP_200_OK, content="OK")