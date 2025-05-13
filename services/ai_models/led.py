from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch


def summarize_led(title, uploader, transcript_text):
    model_id = "pszemraj/led-base-book-summary"
    summarization_pipeline = pipeline(
        task="summarization",
        model=AutoModelForSeq2SeqLM.from_pretrained(model_id),
        tokenizer=AutoTokenizer.from_pretrained(model_id),
        min_length=128,
        max_length=1024,
        do_sample=True,
        temperature=0.3,
        top_k=20,
        top_p=0.8,
        device=0 if torch.cuda.is_available() else -1
    )
    summarizer = HuggingFacePipeline(pipeline=summarization_pipeline)

    # Prompt Template for summarization
    prompt_template = """
    You are a helpful assistant tasked with summarizing YouTube videos.

    Title: "{video_title}"
    Creator/Channel: "{video_uploader}"

    Below is the transcript of the video. Summarize the key points and main ideas clearly and concisely.

    Transcript:
    {video_transcript}

    Summary:
    """

    # Initialize Prompt Template with the video context
    prompt = PromptTemplate(input_variables=["video_title", "video_uploader", "video_transcript"], template=prompt_template)

    chain = prompt | summarizer
    return chain.invoke({
        "video_title": title,
        "video_uploader": uploader,
        "video_transcript": transcript_text
    })