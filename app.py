from utils.summarize import summarize_video
from utils.yt_utils import get_transcript, get_video_id, get_metadata
import gradio as gr

# List of available models
MODEL_OPTIONS = {
    'LED - ( pszemraj/led-base-book-summary )': "LED",
    'BART - ( philschmid/bart-large-cnn-samsum )': "BART"
}


def get_summary(video_id: str, model_choice: str, title: str, channel: str):
    try:
        transcript = get_transcript(video_id)
        try:
            summary = summarize_video(
                title, 
                channel, 
                transcript, 
                MODEL_OPTIONS[model_choice]
            )
            return (transcript, summary)
        except Exception as e:
            gr.Warning("Summary can not be generated due to some technical error!")
            return (None, f"Error: {str(e)}")
    except Exception as e:
        gr.Warning("Video does not have any transcript!")
        return (None, f"Error: {str(e)}")


def validate_url(url: str):
    if url.strip() != "":
        try:
            video_id = get_video_id(url)
            if video_id != None:
                return (
                    gr.Textbox(interactive=False), 
                    video_id
                )
            else:
                gr.Info("Invalid URL!")
        except Exception as e:
            raise gr.Error(f"{str(e)}")
    else:
        gr.Info("URL cannot be empty!")
    return (
        gr.Textbox(interactive=True), 
        None
    )


def fetch_metadata(video_id: str, url: str):
    if video_id != None:
        try:
            data = get_metadata(url)
            return (
                data['thumbnail'], 
                data['title'], 
                data['uploader'], 
                data['description'],
                gr.Button(interactive=True)
            )
        except Exception:
            gr.Warning("Invalid URL! or Video unavailable!")
    return (None, None, None, None, gr.Button(interactive=False))


def disable_buttons():
    return (
        gr.Button(interactive=False),
        gr.ClearButton(interactive=False)
    )


def enable_buttons():
    return (
        gr.Button(interactive=True),
        gr.ClearButton(interactive=True)
    )


def detect_state(state):
    if state == None:
        return gr.ClearButton(interactive=False)
    else:
        return gr.ClearButton(interactive=True)


# Gradio UI

heading = """
<div id="header">
    <p id="title-line">
        <b><span class="red-text">YouTube</span> Summarized</b>
        <i class="subtle-text">with</i>
        <b id="bot">🤖 AI</b>
    </p>
    <p id="made-by">Made by</p>
    <p id="author-link-container">
        <a id="author-link" href="https://www.linkedin.com/in/sobhanbhowmick/" target="_blank">
            <b>Sobhan Bhowmick</b>
        </a>
    </p>
</div>
"""

css = """
#container {
    max-width: 900px;
    margin: 0 auto;
}

#header {
    padding: 1rem;
    text-align: center;
}

#title-line b {
    font-size: 2em;
}

.red-text {
    color: red;
}

.subtle-text {
    color: var(--block-info-text-color);
    margin: 0.5em 0;
}

#bot {
    font-size: 2em;
}

#made-by {
    margin: 0 0 1em 0; 
    color: var(--block-info-text-color);
}

#author-link-container {
    padding: 0 0 0.5em 0;
}

#author-link {
    text-decoration: none;
    color: var(--primary-500);
    border: solid var(--primary-800);
    padding: 5px 15px;
    border-radius: 50px;
}
"""

theme = gr.themes.Default( # type: ignore
    primary_hue="lime",
    neutral_hue="neutral",
    font=gr.themes.GoogleFont("Space Grotesk"), # type: ignore
    font_mono=gr.themes.GoogleFont("JetBrains Mono"), # type: ignore
    text_size=gr.themes.sizes.text_lg, # type: ignore
)

with gr.Blocks(
    title="YouTube Summarized",
    theme=theme,
    css=css,
) as demo:
    gr.Markdown(heading)

    with gr.Column(elem_id="container"):
        with gr.Group():
            url_input = gr.Textbox(
                label="YouTube Video URL",
                info="🔗 Paste the video link ( playlist won't work, obviously! )",
                placeholder="https://youtu.be/xyz...",
                interactive=True,
                max_lines=2,
                autofocus=True,
            )
            model_choice = gr.Radio(
                choices=list(MODEL_OPTIONS.keys()),
                value=list(MODEL_OPTIONS.keys())[0],
                label="Model",
                info="✨ Choose Summarization Model",
            )

        with gr.Row():
            summarize_btn = gr.Button(
                value="Summarize", 
                variant='primary', 
                interactive=False,
                scale=2,
            )
            clear_btn = gr.ClearButton(
                value="Clear", 
                interactive=False,
                scale=1,
            )

        with gr.Row():
            with gr.Column():
                thumbnail_output = gr.Image(
                    label="Thumbnail", 
                    height=262,
                )

            with gr.Column():
                video_title = gr.Textbox(
                    show_label=False, 
                    placeholder="Title...", 
                    lines=1, 
                    max_lines=1,
                )
                channel_name = gr.Textbox(
                    show_label=False, 
                    placeholder="Creator...", 
                    lines=1, 
                    max_lines=1,
                )
                video_desc = gr.TextArea(
                    show_label=False, 
                    placeholder="Description...", 
                    lines=4, 
                    max_lines=4,
                    autoscroll=False,
                )

        with gr.Accordion("Original Transcript", open=False):
            transcript_out = gr.Textbox(
                show_label=False, 
                container=False, 
                lines=15, 
                show_copy_button=True,
            )

        with gr.Row():
            summary_out = gr.Textbox(label="Summary", 
                lines=15, 
                show_copy_button=True
            )

    video_id_state = gr.State(value=None)

    url_input.change(
        fn=validate_url,
        inputs=url_input,
        outputs=[url_input, video_id_state],
        show_progress='hidden',
    )
    
    video_id_state.change(
        fn=fetch_metadata,
        inputs=[video_id_state, url_input],
        outputs=[
            thumbnail_output, 
            video_title, 
            channel_name, 
            video_desc, 
            summarize_btn,
        ]
    ).then(
        fn=detect_state,
        inputs=video_id_state,
        outputs=clear_btn,
    )

    summarize_btn.click(
        fn=disable_buttons,
        inputs=None,
        outputs=[summarize_btn, clear_btn],
    ).then(
        fn=get_summary,
        inputs=[video_id_state, model_choice, video_title, channel_name],
        outputs=[transcript_out, summary_out],
        scroll_to_output=True,
    ).then(
        fn=enable_buttons,
        inputs=None,
        outputs=[summarize_btn, clear_btn],
    )

    clear_btn.click(
        fn=lambda: [
            None, None, None, None, None, None, None, None,
            gr.ClearButton(interactive=False),
        ],
        inputs=None,
        outputs=[
            url_input,
            thumbnail_output,
            video_title,
            channel_name,
            video_desc,
            transcript_out,
            summary_out,
            video_id_state,
            clear_btn,
        ],
    )

if __name__ == "__main__":
    demo.launch(show_error=False)
