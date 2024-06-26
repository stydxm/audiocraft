import time
import random

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
messages = ["the first question", "the first answer", "the second question", "the second answer"]


def generate_clips(*args: list[gr.Textbox]):
    # for i in args:
    #     i.value="example"
    time.sleep(3.7)
    return ["example result"] * len(args)


def mock_cut_clips(*args: list[gr.Textbox]) -> list[gr.Video]:
    time.sleep(2.6)
    return [gr.Video("./api/sora.webm", visible=True, interactive=False)] * len(args)


def mock_fetch_metadata(*args: list[gr.Textbox]):
    time.sleep(2.6)
    return [gr.update(value="Time: 00:03-00:08\nDuration: 5s\nFrame Count: 150")] * len(
        args
    )


def mock_musicgen(*args: list[gr.Audio]) -> list[gr.Audio]:
    time.sleep(5.6)
    return [gr.Audio("./api/generated.wav", label="BGM Generation", interactive=False)] * len(args)


def mock_audiogen(*args: list[gr.Audio]) -> list[gr.Audio]:
    time.sleep(5.6)
    return [gr.Audio("./api/generated.wav", label="Audio Generation", interactive=False)] * len(args)


def mock_tts(*args: list[gr.Audio]) -> list[gr.Audio]:
    time.sleep(5.6)
    return [gr.Audio("./api/generated.wav", label="TTS", interactive=False)] * len(args)


def generate_result():
    time.sleep(7)
    return gr.Video("./api/sora.webm")


def mock_chatbot(*chatbots):
    assert len(messages) % 2 == 0
    for bot in chatbots:
        for round in range(len(messages) // 2):
            bot[round][0] = ""
            bot[round][1] = ""
            for char in messages[round * 2]:
                bot[round][0] += char
                time.sleep(random.uniform(0.03,0.08))
                yield chatbots
            for char in messages[round * 2 + 1]:
                bot[round][1] += char
                time.sleep(random.uniform(0.03,0.08))
                yield chatbots
            time.sleep(random.uniform(0.5,1.0))


with gr.Blocks(
        # title="InternVideo-VideoChat!",
        # theme=gvlabtheme,
        # css="#chatbot {overflow:auto; height:500px;} #InputVideo {overflow:visible; height:320px;} footer {visibility: none}",
) as demo:
    with gr.Row():
        with gr.Column(scale=4, visible=True) as video_upload:
            up_video = gr.Video(interactive=True, include_audio=True)
            upload_button = gr.Button(
                value="Upload", interactive=True, variant="primary"
            )
            video_reset_button = gr.Button("Reset")

        with gr.Column(scale=6, visible=True) as clip_preview:
            video_clips = []
            metadatas = []
            for i in range(1, 5):
                tab = gr.Tab("scene" + str(i))
                tab.__enter__()
                clip_video = gr.Video(interactive=False)
                video_clips.append(clip_video)
                clip_metadata = gr.Textbox(
                    "Please upload first", interactive=False, lines=2
                )
                metadatas.append(clip_metadata)
                tab.__exit__()
            next_button = gr.Button("Next", variant="primary", visible=False)

        with gr.Column(visible=False) as perception_module:
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
            audiogen_outputs = []
            tts_outputs = []
            chatbots = []
            for i in range(1, 5):
                tab = gr.Tab("scene" + str(i))
                tab.__enter__()
                with gr.Row():
                    with gr.Column(scale=6):
                        with gr.Row():
                            clip_chatbot = gr.Chatbot(
                                label="Discussions between Two Agents",
                                value=[[None, None]] * (len(messages) // 2),
                                height="30em",
                            )
                        with gr.Row():
                            with gr.Column():
                                clip_caption = gr.Textbox(
                                    label="Clip Perception",
                                    value="Please upload your video first",
                                    interactive=False,
                                    lines=3
                                )
                                clip_emotion = gr.Textbox(
                                    label="Emotion",
                                    value="emotion",
                                    interactive=False,
                                    lines=3
                                )
                                clip_subtitles = gr.Textbox(
                                    label="Subtitles", value="subtitles", lines=3
                                )
                            with gr.Column():
                                clip_aspects = gr.Textbox(
                                    label="Key Aspects",
                                    value="key aspects",
                                    lines=6
                                )
                                clip_possible_sounds = gr.Textbox(
                                    label="Possible Sounds",
                                    value="possible sounds",
                                    lines=6
                                )
                    chatbots.append(clip_chatbot)
                    text_outputs.append(clip_caption)
                    text_outputs.append(clip_emotion)
                    text_outputs.append(clip_subtitles)
                    text_outputs.append(clip_aspects)

                    with gr.Column(scale=4):
                        gr.Video("./api/sora.webm")
                        audiogen = gr.Audio()
                        audiogen_2 = gr.Audio()
                        tts = gr.Audio()
                    audiogen_outputs.append(audiogen)
                    audiogen_outputs.append(audiogen_2)
                    tts_outputs.append(tts)
                tab.__exit__()

            with gr.Tab("overall"):
                with gr.Row():
                    with gr.Column(scale=6):
                        with gr.Row():
                            overall_chatbot = gr.Chatbot(
                                label="Discussions between Two Agents",
                                value=[["mesage", "response"], ["mesage2", "response2"]],
                                height="20em",
                            )
                        with gr.Row():
                            with gr.Column():
                                overall_caption = gr.Textbox(
                                    label="Overall Caption",
                                    value="Please upload your video first",
                                    interactive=False,
                                    lines=2,
                                )
                                overall_emotion = gr.Textbox(
                                    label="Emotion Variant",
                                    value="emotion variant",
                                    interactive=False,
                                    lines=2,
                                )
                            with gr.Column():
                                clip_aspects = gr.Textbox(
                                    label="Key Aspects", value="key aspects", lines=7
                                )
                        with gr.Row():
                            bgm_description = gr.Textbox(
                                label="BGM Description", value="bgm description", lines=2
                            )

                    with gr.Column(scale=4):
                        full_video = gr.Video("./api/sora.webm")
                        musicgen = gr.Audio(label="BGM Generation", value="./api/generated.wav")

            text_outputs.append(overall_caption)
            # with gr.Column(scale=4, visible=False) as audio_preview:
            #     musicgen = gr.Audio()
            #     audiogen = gr.Audio()
            #     tts = gr.Audio()

            with gr.Row():
                with gr.Column(scale=6):
                    generate_button = gr.Button("Merge", variant="primary")
                with gr.Column(scale=4):
                    preview_reset_button = gr.Button("Reset")

    upload_button.click(mock_cut_clips, video_clips, video_clips)
    upload_button.click(mock_fetch_metadata, metadatas, metadatas)
    upload_button.click(lambda: gr.update(visible=True), None, [next_button])
    next_button.click(mock_chatbot, inputs=chatbots, outputs=chatbots)
    next_button.click(mock_audiogen, audiogen_outputs, audiogen_outputs)
    next_button.click(mock_tts, tts_outputs, tts_outputs)
    next_button.click(generate_clips, text_outputs, text_outputs)
    next_button.click(
        lambda: (
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=True),
        ),
        None,
        [video_upload, clip_preview, perception_module],
    )
    video_reset_button.click(lambda: gr.Video(), None, [up_video])
    generate_button.click(generate_result, None, full_video)
    preview_reset_button.click(
        lambda: (
            gr.update(visible=True),
            gr.update(visible=True),
            gr.update(visible=False),
            gr.Video()
        ),
        None,
        [video_upload, clip_preview, perception_module, up_video],
    )

demo.launch()
