import json
from vosk import Model, KaldiRecognizer

model = Model("vosk-model-ru-0.42")
rec = KaldiRecognizer(model, 24000)

def speach_to_text_func(data : bytes) -> str:
    # print(rec.AcceptWaveform(data))
    if(rec.AcceptWaveform(data)) and (len(data) > 0):
        answer = json.loads(rec.Result())
        if answer['text']:
            return answer['text']
        else: 
            return "null message"
    else:
        return "no accept"