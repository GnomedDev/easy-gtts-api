from io import BytesIO

import fastapi
from gtts import gTTS, gTTSError
from gtts.lang import tts_langs

app = fastapi.FastAPI()
tts_langs = tts_langs()

@app.get("/")
async def root():
    return fastapi.responses.RedirectResponse("/docs")

@app.get("/tts")
def tts(text, lang="en-us"):
    if lang not in tts_langs:
        raise fastapi.HTTPException(status_code=400, detail=f"{lang} is not a valid language code.")

    mp3 = BytesIO()
    gTTS(text=text, lang=lang).write_to_fp(mp3)
    mp3.seek(0)
    return fastapi.responses.StreamingResponse(mp3, media_type="audio/mp3")

@app.get("/v1/tts")
def v1_tts(text, lang="en-us"):
    if lang not in tts_langs:
        raise fastapi.HTTPException(status_code=400, detail=f"{lang} is not a valid language code.")

    mp3 = BytesIO()
    try:
        gTTS(text=text, lang=lang).write_to_fp(mp3)
    except gTTSError as e:
        if e.rsp:
            raise fastapi.HTTPException(
                status_code=e.rsp.status_code,
                detail=e.rsp.content,
                headers=e.rsp.headers
                )

        raise

    mp3.seek(0)
    return fastapi.responses.StreamingResponse(mp3, media_type="audio/mp3")

@app.get("/langs")
@app.get("/v1/langs")
async def get_langs():
    return tts_langs
