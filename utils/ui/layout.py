import gradio as gr

from utils.ui.events import fetch_metadata, get_summary, validate_url
from utils.ui.states import disable_buttons, enable_buttons, detect_state
from utils.ui.theme import heading, theme, css
from utils.ui.constants import MODEL_OPTIONS


def init_layout():
    with gr.Blocks(
        title="YouTube Summarized",
        theme=theme,
        css=css,
    ) as app:
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
    return app
