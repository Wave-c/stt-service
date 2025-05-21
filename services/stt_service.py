import json
import wave
from vosk import Model, KaldiRecognizer, SetLogLevel

model = Model("vosk-model-ru-0.42")

def speach_to_text_func(data : bytes) -> str:
    rec : KaldiRecognizer
    rec = KaldiRecognizer(model, 24000)
    # print(rec.AcceptWaveform(data))
    if(rec.AcceptWaveform(data)) and (len(data) > 0):
        answer = json.loads(rec.Result())
        if answer['text']:
            return answer['text']
        else: 
            return "null message"
    else:
        return "no accept"

def speach_to_text_func1():
    SetLogLevel(0)

    wf = wave.open("buffer.wav", "rb")

    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        return

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            rec.Result()# print()
        else:
            rec.PartialResult()# print()

    result = rec.FinalResult()
    wf.close()
    return json.loads(result)["text"]
