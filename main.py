from io import BytesIO

import fastapi
from gtts import gTTS

app = fastapi.FastAPI()

@app.get("/")
async def root():
    return fastapi.responses.RedirectResponse("/docs")

@app.get("/tts")
def tts(text, lang="en-us"):
    mp3 = BytesIO()
    gTTS(text=text, lang=lang).write_to_fp(mp3)
    mp3.seek(0)
    return fastapi.responses.StreamingResponse(mp3, media_type="audio/mp3")
