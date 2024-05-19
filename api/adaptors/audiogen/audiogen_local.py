import torchaudio
from flask import send_file, Response
from audiocraft.models import AudioGen
from audiocraft.data.audio import audio_write

model = AudioGen.get_pretrained("facebook/audiogen-medium")


def predict(prompt: str, duration: int) -> Response:
    print(f"processing audiogen locally with duration {duration} prompt: " + prompt)

    model.set_generation_params(duration=duration)
    descriptions = [prompt]
    wav = model.generate(descriptions)  # generates 3 samples.

    for idx, one_wav in enumerate(wav):
        # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
        path=audio_write(f'{idx}', one_wav.cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
        send_file(path,as_attachment=True)