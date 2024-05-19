from gradio_client import Client
from flask import send_file, Response

client = Client("https://facebook-musicgen.hf.space/", verbose=False)
# verbose不能开，否则会因为编码问题报错


def predict(prompt: str) -> Response:
    print("processing musicgen by huggingface space with prompt: " + prompt)

    result = client.predict(prompt, None, fn_index=0)
    print(result)
    return send_file(result[1], as_attachment=True)
