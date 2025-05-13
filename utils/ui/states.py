import gradio as gr

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
    if state is None:
        return gr.ClearButton(interactive=False)
    else:
        return gr.ClearButton(interactive=True)

