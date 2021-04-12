from functools import wraps
from io import BytesIO

from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import RedirectResponse, StreamingResponse
from gtts import gTTS, gTTSError
from gtts.lang import tts_langs

app = FastAPI()
tts_langs = tts_langs()

def verify_lang(func):
    @wraps(func)
    def replace_func(text, lang="en"):
        if lang not in tts_langs:
            raise HTTPException(
                detail=f"{lang} is not a valid language code.",
                status_code=400
                )

        return func(text, lang)

    return replace_func

@app.get("/")
async def root():
    return RedirectResponse("/docs")

@verify_lang
@app.get("/tts")
def tts(text, lang="en"):
    mp3 = BytesIO()
    gTTS(text=text, lang=lang).write_to_fp(mp3)
    mp3.seek(0)

    return StreamingResponse(mp3, media_type="audio/mp3")

@verify_lang
@app.get("/v1/tts")
def v1_tts(text, lang="en"):
    mp3 = BytesIO()
    try:
        gTTS(text=text, lang=lang).write_to_fp(mp3)
    except (AssertionError, ValueError, RuntimeError) as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except gTTSError as e:
        if e.rsp is not None:
            headers = e.rsp.headers
            headers.pop("Content-Length", None)

            raise HTTPException(
                status_code=e.rsp.status_code,
                detail=e.rsp.content.decode(),
                headers=headers
                )

        raise

    mp3.seek(0)
    return StreamingResponse(mp3, media_type="audio/mp3")

@app.post("/v1/tts")
def v1_tts_post(text: str = Body(...), lang: str = Body(default="en")):
    return v1_tts(text, lang)

@app.get("/langs")
@app.get("/v1/langs")
async def get_langs():
    return tts_langs
