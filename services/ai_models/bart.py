from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from nltk.tokenize import sent_tokenize
import nltk
import torch


nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)


def chunk_by_sentences(text, tokenizer, max_tokens=800):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        test_chunk = current_chunk + " " + sentence
        if len(tokenizer.encode(test_chunk)) < max_tokens:
            current_chunk = test_chunk
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


def summarize_bart(title, uploader, transcript_text):
    model_id = "philschmid/bart-large-cnn-samsum"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
    summarizer = pipeline(
        "summarization",
        model=model,
        tokenizer=tokenizer,
        device=0 if torch.cuda.is_available() else -1
    )

    chunks = chunk_by_sentences(transcript_text, tokenizer,)

    summaries = []
    for chunk in chunks:
        prompt = f"Summarize the following transcript chunk of a video titled '{title}' by '{uploader}':\n{chunk}"
        result = summarizer(prompt, max_length=256, min_length=64, do_sample=False)
        summaries.append(result[0]['summary_text'])
        
    # Combine and summarize all summaries
    final_input = " ".join(summaries)
    final_summary = summarizer(f"Create a final summary of this video from these chunk summaries:\n{final_input}",
                               max_length=512, min_length=128, do_sample=False)
    return final_summary[0]['summary_text']