import os
import gradio as gr
import masking
import re
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

genai.configure(api_key = os.getenv('GEMINI_API_KEY'))

model = genai.GenerativeModel('gemini-2.0-flash-exp')

custom_button = """
<style>
    #gemini_submit {
        margin: 0.5em 0em 0.5em 0.1em;
        max-width: 3em;
        min-width: 3em !important;
        height: 3em;
        background-image: url('https://img.icons8.com/fluency-systems-filled/48/sent.png');
        background-size: cover;
        background-repeat: no-repeat;
        border: none;
        background-position: center center;
        background-size: 25px;
        border-radius: 50%;
    }

    #gemini_clear{
        margin: 0.5em 0em 0.5em 0.1em;
        max-width: 3em;
        min-width: 3em !important;
        height: 3em;
        background-image: url('https://img.icons8.com/ios-filled/50/synchronize.png');
        background-size: cover;
        background-repeat: no-repeat;
        border: none;
        background-position: center center;
        background-size: 25px;
        border-radius: 50%;
    }

    #gemini_chat {
        height: 490px !important;
    }
</style>
"""

custom_head = """
<iframe style="display:none" onload="
    document.title = 'DataGuard';
    var link = document.querySelector('link[rel=icon]') || document.createElement('link');
    link.rel = 'icon';
    link.href = 'https://cdn-icons-png.flaticon.com/512/6356/6356296.png';
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
    <hr style="padding-bottom: 0px;">
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

def handle_user_query(msg, chatbot):
    if(not (msg.isspace() or msg == '')):
        chatbot += [[process_input(msg), None]]
    return ('', chatbot)

def handle_gemini_response(chatbot):
    query = chatbot[-1][0]
    formatted_chatbot = generate_chatbot(chatbot[:-1])
    chat = model.start_chat(history = formatted_chatbot)
    response = chat.send_message(query)
    chatbot[-1][1] = response.text
    return (chatbot)

def generate_chatbot(chatbot: list[list[str, str]]) -> list[list[str, str]]:
    formatted_chatbot = []
    if len(chatbot) == 0:
        return formatted_chatbot
    for ch in chatbot:
        formatted_chatbot.append(
            {
                "role": "user",
                "parts": [ch[0]]
            }
        )
        formatted_chatbot.append(
            {
                "role": "model",
                "parts": [ch[1]]
            }
        )
    return formatted_chatbot

def clear_function() -> tuple:
    return '', ''

def gradio_interface():
    with gr.Blocks(theme = gr.themes.Soft(primary_hue="cyan"), fill_width = False) as interface:
        gr.HTML(custom_head)
        gr.HTML(custom_title)
        gr.HTML(custom_footer)
        gr.HTML(custom_button)
        with gr.Tab(label = 'Masking-Only'):
            with gr.Column():
                with gr.Row():
                    input_txt = gr.components.Textbox(label = 'Raw Input', placeholder = "Enter text here...", autofocus = True, lines = 20)
                    output_txt = gr.components.Textbox(label = 'Masked Output', show_copy_button = True, lines =20)
                with gr.Row():
                    submit = gr.components.Button(value = 'Submit', variant = 'primary')
                    clear = gr.components.Button(value = 'Clear', variant = 'stop')
            submit.click(process_input, [input_txt], [output_txt])
            clear.click(clear_function, [], [input_txt, output_txt])
        with gr.Tab(label = 'Masked-Gemini'):
            chatbot = gr.Chatbot(
                label = 'Chat with Gemini',
                bubble_full_width = False,
                show_copy_button = True,
                show_label = False,
                elem_id = 'gemini_chat',
                placeholder = 'What can I help you with?'
            )
            with gr.Row():
                clear = gr.ClearButton(elem_id = 'gemini_clear', value = '')
                msg = gr.Textbox(show_label = False, elem_id = 'gemini_text', placeholder = 'Ask Gemini')
                clear.add([msg, chatbot])
                submit = gr.components.Button(value = '', variant = 'primary', elem_id = 'gemini_submit')
            msg.submit(
                handle_user_query,
                [msg, chatbot],
                [msg, chatbot]
            ).then(
                handle_gemini_response,
                [chatbot],
                [chatbot]
            )

            submit.click(
                handle_user_query,
                [msg, chatbot],
                [msg, chatbot]
            ).then(
                handle_gemini_response,
                [chatbot],
                [chatbot]
            )

    interface.launch(share = False, show_api = False)