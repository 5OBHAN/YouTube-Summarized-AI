# YouTube Summarized 📜🪄

_A lightweight Python application to summarize YouTube videos, using Hugging Face transformer models — all via a clean, feature-rich & user-friendly Gradio GUI._

## ✨ Features

- ✅ Summarize long videos (using chunking)
- ✅ Choose between multiple summarization models
- ✅ Fetch auto/manual transcripts and translate (to english) if needed
- ✅ Displays original transcript of the video (in english)
- ✅ Clean, feature-rich and user-friendly GUI using Gradio

## 🕹️ Usage

```bash
# 1. Install dependencies
pip install -r requirements.txt
```

```bash
# 2. Login to Hugging Face (by using an Access Token from your account)
huggingface-cli login
```

> **Creating new tokens:** https://huggingface.co/settings/tokens
>
> **Learn more:** https://huggingface.co/docs/hub/security-tokens#user-access-tokens


```bash
# 3. Run the application
python app.py
```

```bash
# 4. Visit the local URL
http://127.0.0.1:7860  # Usually
```

## ⚖️ License

_This project is licensed under the_ **[GNU General Public License v3.0](LICENSE)**
