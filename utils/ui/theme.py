import gradio as gr

heading = """
<div id="header">
    <p id="title-line">
        <b><span class="red-text">YouTube</span> Summarized</b>
        <i class="subtle-text">with</i>
        <b id="bot">AI 🤖</b>
    </p>
    <p id="made-by">Developed by</p>
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
    color: #0088df;
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
