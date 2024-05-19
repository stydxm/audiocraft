# AudioCraft API
Flask based HTTP API on top of audiocraft and huggingface spaces

## API references
### MusicGen
endpoint: `/musicgen`
method: GET

|params|possible values|notes|
|:-:|:-:|:-:|
|mode|`hf` `local` `gradio`|gradio mode runs locally with `demos/musicgen_app.py`|
|prompt|your prompt||
|duration|int|not avaiable in hf mode|

### AudioGen
endpoint: `/audiogen`
method: GET

|params|possible values|notes|
|:-:|:-:|:-:|
|prompt|your prompt||
|duration|int|not avaiable in hf mode|

### TTS
endpoint: `/tts`
method: GET

|params|possible values|notes|
|:-:|:-:|:-:|
|model|`xtts` `openvoice`|more will be available in the future|
|prompt|your prompt||
|language|could be found in each .py file|change with different models|