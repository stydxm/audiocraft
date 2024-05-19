# python -m demos.musicgen_app --share
from gradio_client import Client, file
from flask import send_file, Response

client = Client("http://127.0.0.1:7860/", verbose=False)
# verbose不能开，否则会因为编码问题报错


def predict(prompt: str, duration: int) -> Response:
    print(
        f"processing musicgen by huggingface space with duration {duration} prompt: "
        + prompt
    )
    result = client.predict(
        model_path="/root/works/music/audiocraft/models/musicgen-melody",
        decoder="Default",
        text=prompt,
        melody=file(
            "https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav"
        ),
        duration=duration,
        topk=250,
        topp=0,
        temperature=1,
        cfg_coef=3,
        api_name="/predict_full",
    )
    return send_file(result, as_attachment=True)
