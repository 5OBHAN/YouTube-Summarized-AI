import gradio as gr

from utils.ui.constants import MODEL_OPTIONS
from utils.yt_utils import get_transcript, get_video_id, get_metadata
from services.summarize import summarize_video


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
            if video_id is not None:
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
    if video_id is not None:
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


