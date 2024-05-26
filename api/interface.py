import time

import gradio as gr
from gradio.themes import Base, colors, sizes, GoogleFont

gvlabtheme = Base(
    primary_hue=colors.blue,
    secondary_hue=colors.sky,
    neutral_hue=colors.gray,
    spacing_size=sizes.spacing_md,
    radius_size=sizes.radius_sm,
    text_size=sizes.text_md,
    font=(
        GoogleFont("Noto Sans"),
        "ui-sans-serif",
        "sans-serif",
    ),
    font_mono=(
        GoogleFont("IBM Plex Mono"),
        "ui-monospace",
        "monospace",
    ),
)


def upload_video(*args: list[gr.Textbox]):
    # for i in args:
    #     i.value="example"
    time.sleep(3.7)
    return ["example result"] * len(args)


def mock_audio_generation():
    time.sleep(5.6)
    return (
        gr.Audio(
            "./api/generated.wav",
            label="BGM Generation",
        ),
        gr.Audio(
            "./api/generated.wav",
            label="Audio Generation",
        ),
        gr.Audio(
            "./api/generated.wav",
            label="TTS",
        ),
    )


def generate_result():
    time.sleep(7)
    return gr.Video("./api/sora.webm")


with gr.Blocks(
    # title="InternVideo-VideoChat!",
    # theme=gvlabtheme,
    # css="#chatbot {overflow:auto; height:500px;} #InputVideo {overflow:visible; height:320px;} footer {visibility: none}",
) as demo:
    with gr.Row():
        with gr.Column(scale=4, visible=True) as video_upload:
            up_video = gr.Video(
                interactive=True, include_audio=True, elem_id="video_upload"
            )
            upload_button = gr.Button(
                value="Upload", interactive=True, variant="primary"
            )
            video_reset_button = gr.Button("Reset")

        with gr.Column(scale=6, visible=True) as perception_module:
            # with gr.Row():
            #     with gr.Column(scale=7):
            #         text_input = gr.Textbox(
            #             show_label=False,
            #             placeholder="Please upload your video first",
            #             interactive=False,
            #         )
            # with gr.Column(scale=3, min_width=0):
            #     run = gr.Button("Send")
            text_outputs = []
            for i in range(1, 5):
                tab = gr.Tab("scene" + str(i), elem_id="scene" + str(i))
                tab.__enter__()
                with gr.Row():
                    clip_chatbot = gr.Chatbot(
                        elem_id="chatbot",
                        label="Discussions between Two Agents",
                        height="10em",
                    )
                with gr.Row():
                    with gr.Column():
                        clip_caption = gr.Textbox(
                            label="Clip Perception",
                            value="Please upload your video first",
                            interactive=False,
                            lines=2
                        )
                        clip_emotion = gr.Textbox(label="Emotion",value="emotion", interactive=False,lines=2)
                        clip_subtitles = gr.Textbox(
                            label="Subtitles", value="subtitles",lines=2
                        )
                    with gr.Column():
                        clip_aspects = gr.Textbox(
                            label="Key Aspects", value="key aspects",lines=2,scale=2
                        )
                        clip_possible_sounds = gr.Audio(
                            label="Possible Sounds", value="./api/generated.wav",scale=1
                        )
                text_outputs.append(clip_caption)
                text_outputs.append(clip_emotion)
                text_outputs.append(clip_subtitles)
                text_outputs.append(clip_aspects)
                tab.__exit__()

            with gr.Tab("overall", elem_id="overall"):
                with gr.Row():
                    overall_chatbot = gr.Chatbot(
                        elem_id="chatbot",
                        label="Discussions between Two Agents",
                        height="10em",
                    )
                with gr.Row():
                    with gr.Column():
                        overall_caption = gr.Textbox(
                            label="Overall Caption",
                            value="Please upload your video first",
                            interactive=False,
                            lines=2
                        )
                        overall_emotion = gr.Textbox(label="Emotion Variant",value="emotion variant", interactive=False,lines=2)
                    with gr.Column():
                        clip_aspects = gr.Textbox(label="Key Aspects", value="key aspects",lines=7)
                with gr.Row():
                    bgm_description=gr.Textbox(label="BGM Description", value="bgm description",lines=2)
            text_outputs.append(overall_caption)
        with gr.Column(scale=4, visible=False) as audio_preview:
            musicgen = gr.Audio()
            audiogen = gr.Audio()
            tts = gr.Audio()
            generate_button = gr.Button("Generate", variant="primary")

        with gr.Column(scale=6, visible=False) as result:
            video_result = gr.Video()
            reset_button = gr.Button("Reset All")

    upload_button.click(
        lambda: (gr.update(visible=False), gr.update(visible=True)),
        None,
        [video_upload, audio_preview],
    )
    upload_button.click(upload_video, text_outputs, text_outputs)
    upload_button.click(mock_audio_generation, None, [musicgen, audiogen, tts])
    video_reset_button.click(lambda: gr.Video(), None, [up_video])
    # generate_button.click(generate, None, [result])
    generate_button.click(
        lambda: (gr.update(visible=False), gr.update(visible=True)),
        None,
        [perception_module, result],
    )
    generate_button.click(generate_result, None, video_result)
    reset_button.click(
        lambda: (
            gr.update(visible=True),
            gr.update(visible=True),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.Video(interactive=True, include_audio=True, elem_id="video_upload"),
        ),
        None,
        [video_upload, perception_module, audio_preview, result, up_video],
    )

demo.launch()
