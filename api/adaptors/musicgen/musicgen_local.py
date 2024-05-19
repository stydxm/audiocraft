import torchaudio
from flask import send_file, Response
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write

model = MusicGen.get_pretrained("facebook/musicgen-melody")


def predict(prompt: str, duration: int) -> Response:
    print(f"processing musicgen locally with duration {duration} prompt: " + prompt)

    model.set_generation_params(duration=duration)
    wav = model.generate_unconditional(4)
    descriptions = [prompt]
    wav = model.generate(descriptions)

    melody, sr = torchaudio.load("./assets/bach.mp3")
    wav = model.generate_with_chroma(descriptions, melody[None].expand(3, -1, -1), sr)
    for idx, one_wav in enumerate(wav):
        # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
        path = audio_write(
            f"{idx}",
            one_wav.cpu(),
            model.sample_rate,
            strategy="loudness",
            loudness_compressor=True,
        )
        return send_file(path, as_attachment=True)
