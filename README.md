# gTTAPI

An easy to use gTTS middleman using FastAPI, hosted at https://easy-gtts.herokuapp.com

## GET /
Returns documentation
## GET /tts
Returns TTS from gTTS, params are:
* `?text=`: Text to TTS, required
* `?lang=en-us`: Language of text, default en-us
### Example
`https://easy-gtts.herokuapp.com/tts?text=Hello%20World&lang=en-gb`
