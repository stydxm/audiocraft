import gradio as gr
from gradio.themes import Base, colors, sizes, GoogleFont
import time
import os

title = """<h1 align="center"><a href="https://github.com/OpenGVLab/Ask-Anything"><img src="https://s1.ax1x.com/2023/05/07/p9dBMOU.png" alt="Ask-Anything" border="0" style="margin: 0 auto; height: 100px;" /></a> </h1>"""
description = """
        VideoChat2 powered by InternVideo!<br><p><a href='https://github.com/OpenGVLab/Ask-Anything'><img src='https://img.shields.io/badge/Github-Code-blue'></a></p><p>
        """
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
            with gr.Column(elem_id="image") as img_part:
                up_video = gr.Video(
                    interactive=True, include_audio=True, elem_id="video_upload"
                )
            upload_button = gr.Button(
                value="Upload", interactive=True, variant="primary"
            )

        with gr.Column(scale=6, visible=True) as perception_module:
            with gr.Tab("overall", elem_id="overall"):
                overall_caption = gr.Textbox(
                    label="Overall Caption",
                    value="Please upload your video first",
                    interactive=False,
                    lines=2,
                )
                chatbot = gr.Chatbot(elem_id="chatbot", label="Key Aspects")
                # with gr.Row():
                #     with gr.Column(scale=7):
                #         text_input = gr.Textbox(
                #             show_label=False,
                #             placeholder="Please upload your video first",
                #             interactive=False,
                #         )
                # with gr.Column(scale=3, min_width=0):
                #     run = gr.Button("Send")
            outputs = [overall_caption]
            for i in range(1, 5):
                tab = gr.Tab("scene" + str(i), elem_id="scene" + str(i))
                tab.__enter__()
                clip_perception = gr.Textbox(
                    label="Clip Perception",
                    value="Please upload your video first",
                    interactive=False,
                    lines=2,
                )
                chatbot = gr.Chatbot(elem_id="chatbot", label="Key Aspects")
                outputs.append(clip_perception)
                tab.__exit__()
        with gr.Column(scale=4, visible=False) as audio_preview:
            musicgen = gr.Audio()
            audiogen = gr.Audio()
            tts = gr.Audio()
            generate_button = gr.Button("Generate", variant="primary")

        with gr.Column(scale=6, visible=False) as result:
            video_result = gr.Video()

    reset_button = gr.Button("Reset")

    upload_button.click(
        lambda: (gr.update(visible=False), gr.update(visible=True)),
        None,
        [video_upload, audio_preview],
    )
    upload_button.click(upload_video, outputs, outputs)
    upload_button.click(mock_audio_generation, None, [musicgen, audiogen, tts])
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
