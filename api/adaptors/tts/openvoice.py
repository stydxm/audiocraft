from gradio_client import Client
from flask import send_file, Response

client = Client("https://myshell-ai-openvoicev2.hf.space/--replicas/nx4jp/")


def predict(prompt: str, language: str) -> Response:

    if language not in [
        "en_default",
        "en_us",
        "en_br",
        "en_au",
        "en_in",
        "es_default",
        "fr_default",
        "jp_default",
        "zh_default",
        "kr_default",
    ]:
        return Response("wrong language")

    print("processing xtts by huggingface space with prompt: " + prompt)
    result = client.predict(
        prompt,  # str  in 'Text Prompt' Textbox component
        language,  # str (Option from: [('en_default', 'en_default'), ('en_us', 'en_us'), ('en_br', 'en_br'), ('en_au', 'en_au'), ('en_in', 'en_in'), ('es_default', 'es_default'), ('fr_default', 'fr_default'), ('jp_default', 'jp_default'), ('zh_default', 'zh_default'), ('kr_default', 'kr_default')]) in 'Style' Dropdown component
        "https://myshell-ai-openvoicev2.hf.space/--replicas/nx4jp/file=/tmp/gradio/971e5614c2398ed64e7c476251ec42cdb699d033/speaker0.mp3",  # str (filepath on your computer (or URL) of file) in 'Reference Audio' Audio component
        True,  # bool  in 'Agree' Checkbox component
        fn_index=1,
    )
    print(result)
    return send_file(result[1], as_attachment=True)
