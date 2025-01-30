import gradio as gr
import masking

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
<div">
    <img src="https://cdn-icons-png.flaticon.com/512/6356/6356296.png" alt="Logo" style="display: block; margin: 0 auto; width: 80px; height: 80px; padding: 0px;">
    <h1 style="color: White; text-align: center; font-size: 35px;">
        DATAGUARD
    </h1>
    <hr style = "padding-bottom: 40px;">
</div>
"""

custom_footer = """
<style>
    footer {display: none !important;}
</style>
"""

def process_input(inp):
    inp = masking.mask_using_phonenumbers(inp)

    inp = masking.mask_using_regex(inp)

    inp = masking.mask_using_NER(inp)

    return (inp)

def gradio_interface():
    with gr.Blocks(theme = gr.themes.Soft(primary_hue="cyan")) as interface:
        gr.HTML(custom_head)
        gr.HTML(custom_title)
        gr.HTML(custom_footer)
        subinterface1 = gr.Interface(fn=process_input, inputs=[gr.Textbox(label = 'Raw Input', placeholder = "Enter input...", autofocus = True, lines = 20)],
                            outputs=[gr.Textbox(label = 'Masked Output', show_copy_button = True, lines =20)],
                            allow_flagging="never")

    interface.launch(share = False, show_api = False)