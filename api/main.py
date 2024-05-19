from flask import Flask, request
from adaptors.musicgen import musicgen_hf, musicgen_local, musicgen_gradio
from adaptors.audiogen import audiogen_local
from adaptors.tts import xtts, openvoice

app = Flask(__name__)


@app.route("/musicgen")
def musicgen():
    prompt = request.args.get("prompt")
    duration = int(request.args.get("duration", "15"))
    mode = request.args.get("mode", "hf")
    if not prompt:
        return "missing prompt"
    print(prompt)
    match mode:
        case "hf":
            return musicgen_hf.predict(prompt)
        case "local":
            return musicgen_local.predict(prompt, duration)
        case "gradio":
            return musicgen_gradio.predict(prompt, duration)


@app.route("/audiogen")
def audiogen():
    prompt = request.args.get("prompt")
    duration = int(request.args.get("duration", "15"))
    if not prompt:
        return "missing prompt"
    return audiogen_local.predict(prompt, duration)


@app.route("/tts")
def tts():
    prompt = request.args.get("prompt")
    language = request.args.get("language", "en")
    mode = request.args.get("mode", "xtts")
    if not prompt:
        return "missing content"
    match mode:
        case "xtts":
            return xtts.predict(prompt, language)
        case "openvoice":
            return openvoice.predict(prompt, language)


if __name__ == "__main__":
    app.run(debug=True)
