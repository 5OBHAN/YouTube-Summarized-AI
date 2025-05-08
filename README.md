# YouTube-Summarized 📜✨

A lightweight Python application to fetch transcripts and metadata from YouTube videos, then summarize them using Hugging Face transformer models — all via a clean Gradio GUI.

## ⚙️ Features

- ✅ Extract YouTube video metadata (title, channel, thumbnail)
- ✅ Fetch auto/manual transcripts and translate if needed
- ✅ Summarize long videos using chunking
- ✅ Choose between LED (fast) or BART (accurate) summarization models
- ✅ Clean and user-friendly GUI using Gradio

## 🖥️ Usage

```bash
# Install dependencies
pip install -r requirements.txt
```

```bash
# Run the Gradio app
python app.py
```