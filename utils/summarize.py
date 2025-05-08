from models.led_model import summarize_led
from models.bart_model import summarize_bart

def summarize_video(title, uploader, transcript, model_choice):
    if model_choice == "LED":
        return summarize_led(title, uploader, transcript)
    elif model_choice == "BART":
        return summarize_bart(title, uploader, transcript)
    else:
        raise ValueError("Invalid model choice")