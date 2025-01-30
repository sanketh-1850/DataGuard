import gradio as gr
import masking
import re

custom_head = """
<iframe style="display:none" onload="
    document.title = 'DataGuard';
    var link = document.querySelector('link[rel=icon]') || document.createElement('link');
    link.rel = 'icon';
    link.href = 'https://cdn-icons-png.flaticon.com/512/6356/6356296.png';  // Replace with your favicon URL
    document.head.appendChild(link);
"></iframe>
"""

custom_title = """
<div>
    <img src="https://cdn-icons-png.flaticon.com/512/6356/6356296.png" alt="Logo" style="display: block; margin: 0 auto; width: 80px; height: 80px; padding: 0px;">
    <h1 style="color: White; text-align: center; font-size: 35px;">
        DATAGUARD
    </h1>
    <p style="color: White; text-align: center; font-size: 20px; margin-top: 10px;">
        Protecting Privacy, Empowering Data.
    </p>
    <hr style="padding-bottom: 40px;">
</div>
"""

custom_footer = """
<style>
    footer {display: none !important;}
</style>
"""


def process_input(inp: str) -> str:
    inp = masking.mask_using_phonenumbers(inp)

    inp = masking.mask_using_regex(inp)

    inp = masking.mask_using_NER(inp)

    return (inp)

def clear_function() -> tuple:
    return '', ''

def gradio_interface():
    with gr.Blocks(theme = gr.themes.Soft(primary_hue="cyan"), fill_width = True) as interface:
        gr.HTML(custom_head)
        gr.HTML(custom_title)
        gr.HTML(custom_footer)
        with gr.Column():
            with gr.Row():
                input_txt = gr.components.Textbox(label = 'Raw Input', placeholder = "Enter text here...", autofocus = True, lines = 20)
                output_txt = gr.components.Textbox(label = 'Masked Output', show_copy_button = True, lines =20)
            with gr.Row():
                submit = gr.components.Button(value = 'Submit', variant = 'primary')
                clear = gr.components.Button(value = 'Clear', variant = 'stop')
        submit.click(process_input, [input_txt], [output_txt])
        clear.click(clear_function, [], [input_txt, output_txt])

    interface.launch(share = False, show_api = False)