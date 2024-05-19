from gradio_client import Client
from flask import send_file, Response

client = Client("https://coqui-xtts.hf.space/--replicas/4o4qk/", verbose=False)


def predict(prompt: str, language: str) -> Response:

    if language not in [
        "en",
        "es",
        "fr",
        "de",
        "it",
        "pt",
        "pl",
        "tr",
        "ru",
        "nl",
        "cs",
        "ar",
        "zh-cn",
        "ja",
        "ko",
        "hu",
        "hi",
    ]:
        return Response("wrong language")

    print("processing xtts by huggingface space with prompt: " + prompt)

    result = client.predict(
        prompt,  # str  in 'Text Prompt' Textbox component
        language,  # str (Option from: [('en', 'en'), ('es', 'es'), ('fr', 'fr'), ('de', 'de'), ('it', 'it'), ('pt', 'pt'), ('pl', 'pl'), ('tr', 'tr'), ('ru', 'ru'), ('nl', 'nl'), ('cs', 'cs'), ('ar', 'ar'), ('zh-cn', 'zh-cn'), ('ja', 'ja'), ('ko', 'ko'), ('hu', 'hu'), ('hi', 'hi')]) in 'Language' Dropdown component
        "https://coqui-xtts.hf.space/--replicas/4o4qk/file=/tmp/gradio/1fb634c95ee60911623727afa0a2ee3948de455b/female.wav",  # str (filepath on your computer (or URL) of file) in 'Reference Audio' Audio component
        None,  # str (filepath on your computer (or URL) of file) in 'Use Microphone for Reference' Audio component
        False,  # bool  in 'Use Microphone' Checkbox component
        False,  # bool  in 'Cleanup Reference Voice' Checkbox component
        False,  # bool  in 'Do not use language auto-detect' Checkbox component
        True,  # bool  in 'Agree' Checkbox component
        fn_index=1,
    )
    print(result)
    return send_file(result[1], as_attachment=True)
