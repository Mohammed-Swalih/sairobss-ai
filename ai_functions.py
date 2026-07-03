from os import close
import tts_accelerator
import pyautogui
import streamlit as st
from numpy.ma.core import count
from streamlit import image
from streamlit_option_menu import option_menu
import time
from groq import Groq
import asyncio
import edge_tts
from playsound import playsound
import os
import speech_recognition as sr
import json
import requests
import io
from PIL import Image, UnidentifiedImageError
from huggingface_hub import InferenceClient
import pywhatkit
import datetime
import requests
from gradio_client import Client
from streamlit_lottie import st_lottie
import imageio
import firebase_admin
from firebase_admin import credentials, db

AI_LOGO= Image.open('Images/SAIROBSS_LOGO_NEW_LOGO.png')
voice_preset = 'en-US-AndrewNeural'
proceed = False
img_generation_count = 0
show_start_hide_stop = True
is_tab_change = True
chat_disable = False
print('Repeating entire')
for img in os.listdir('Images'):
    if 'generated_image' in img:
        os.remove(f'Images/{img}')

if not firebase_admin._apps:
    cred = credentials.Certificate('.venv/Lib/site-packages/FIREBASE_SECRET/sairobss-sync-cloud-firebase-adminsdk-fbsvc-30f1dd1013.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://sairobss-sync-cloud-default-rtdb.firebaseio.com/'
    })


def load_chat_from_json(filename="chat_history.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Chat file not found.")
        return []

def save_chat_to_json(chat_history, filename="chat_history.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, indent=2)

def check_message(event):
    # Get the latest message from 'messages/app'
    check_ref = db.reference('SAIROBSS_SYNC_CHAT/App')
    message = check_ref.get()
    try:
        message = json.loads(message)
    except (json.JSONDecodeError, TypeError):
        pass
    st.session_state.chat_history = load_chat_from_json()
    # Get the value stored at 'messages/app'
    if message:
        with open('ai_app_message_id.txt', "r", encoding="utf-8") as f:
            last_message_id = f.read()
        f.close()
        print(message)
        if message == '!CLEAR!':
            clear_chat_history()
            ref = db.reference('SAIROBSS_SYNC_CHAT/App')
            ref.delete()
            website_conversation('', '')
            with open('ai_app_message_id.txt', "w") as f:
                f.write("0")
            f.close()
        else:
            ai_app_response = ask_ai_chat(message, for_app = True)
            reply_ref = db.reference('SAIROBSS_SYNC_CHAT/AI')
            if 'tool_call' not in ai_app_response and 'tool call' not in ai_app_response:
                if '\n' in ai_app_response or '**' in ai_app_response or '```' in ai_app_response:
                    report = ai_app_response.replace('\n', '<br>').replace('**', '<b>').replace('```', '<code>')
                    bold_fixed_count = 0
                    bold_fixed_report = ''
                    for i in range(len(report)):
                        if report[i] == '<' and report[i + 1] == 'b' and report[i + 2] == '>':
                            if bold_fixed_count % 2 != 0:
                                bold_fixed_report += '</'
                            else:
                                bold_fixed_report += '<'
                            bold_fixed_count += 1
                        else:
                            bold_fixed_report += report[i]

                    quoted = f"I{int(last_message_id) + 1}~{bold_fixed_report}"
                    reply_ref.set(quoted)
                else:
                    quoted = json.dumps(f"I{int(last_message_id) + 1}~{ai_app_response}")
                    reply_ref.set(quoted)
            else:
                if '<tool_call>' in ai_app_response:
                    input_string = ai_app_response.replace('<tool_call>', '').replace('</tool_call>', '')
                    data = json.loads(input_string)
                    tool_name = data['name']
                    tool_description = data["arguments"]["description"]

                    if tool_name == 'generate_image':
                        quoted = json.dumps(f"I{int(last_message_id) + 1}~Cannot generate images.")
                        reply_ref.set(quoted)
                    elif tool_name == 'sleep_cutoff':
                        quoted = json.dumps(f"I{int(last_message_id) + 1}~{tool_description}")
                        reply_ref.set(quoted)
                    elif tool_name == 'play':
                        play_chat(tool_description)
                    elif tool_name == 'air_quality_analyze':
                        report = air_quality_analyze_app().replace('\n', '<br>').replace('**', '<b>')
                        bold_fixed_count = 0
                        bold_fixed_report = ''
                        for i in range(len(report)):
                            if report[i] == '<' and report[i+1] == 'b' and report[i+2] == '>':
                                if bold_fixed_count % 2 != 0:
                                    bold_fixed_report += '</'
                                else:
                                    bold_fixed_report += '<'
                                bold_fixed_count += 1
                            else:
                                bold_fixed_report += report[i]

                        quoted = json.dumps(f"I{int(last_message_id) + 1}~{bold_fixed_report}")
                        reply_ref.set(quoted)

            with open('ai_app_message_id.txt', "w", encoding="utf-8") as f:
                f.write(str(int(last_message_id)+1))
            f.close()
    else:
        print("No new message.")

def change_proceed_state(state):
    global proceed
    proceed = state

def air_quality_analyze_app():
    voc = 300
    eco2 = 10
    aiq = 1
    ai_analyzed_output = ask_ai_chat(f'Can you do 2nd degree air purity analysis. TVOC = {voc}, eCO2 = {eco2}, AIQ = {aiq}', save = False)
    return ai_analyzed_output

def air_quality_analyze_speak():
    voc = 6010
    eco2 = 2000
    aiq = 4
    ai_analyzed_output = ask_ai_chat(f'Can you do 2nd degree air purity analysis. TVOC = {voc}, eCO2 = {eco2}, AIQ = {aiq}', save = False)
    website_conversation('', ai_analyzed_output)
    speak(ai_analyzed_output)

def air_quality_analyze_chat():
    voc = 1500
    eco2 = 1000
    aiq = 5

    st.markdown("""
        <style>
        .glow-wrap {
            font-size: 20px;
            font-weight: bold;
            color: black;
            position: relative;
            display: inline-block;
            margin: 10px 10px;
        }

        .glow-mask {
            background: linear-gradient(
                90deg,
                black 0%,
                white 50%,
                black 100%
            );
            background-size: 200% auto;
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
            animation: shimmer 2s linear infinite;
        }

        @keyframes shimmer {
            0% {
                background-position: -100% center;
            }
            100% {
                background-position: 100% center;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # Show "Scanning..."
    placeholder = st.empty()

    # Show scanning
    with placeholder:
        st.markdown('<div class="glow-wrap"><span class="glow-mask">Scanning...</span></div>', unsafe_allow_html=True)

    time.sleep(3)

    with placeholder:
        st.markdown('<div class="glow-wrap"><span class="glow-mask">Analyzing...</span></div>',
                    unsafe_allow_html=True) # You can use this to clear it if needed
    time.sleep(3)
    placeholder.empty()

    ai_analyzed_output = ask_ai_chat(f'Can you do 2nd degree air purity analysis. TVOC = {voc}, eCO2 = {eco2}, AIQ = {aiq}', save = False)
    website_conversation('', ai_analyzed_output)

def date_find_speak():
    date_set = datetime.date.today()
    date_today = date_set.strftime('%d %B %Y')
    website_conversation('', f'The date today is {date_today}')
    st.session_state.chat_history.append({"role": "assistant", "content": f'The date today is {date_today}'})
    save_chat_to_json(st.session_state.chat_history)
    speak(f'The date today is {date_today}')

def time_find_speak():
    time_set = datetime.datetime.now()
    time_now = time_set.strftime('%I:%M %p')
    website_conversation('', f'the time now is {time_now}')
    st.session_state.chat_history.append({"role": "assistant", "content": f'the time now is {time_now}'})
    save_chat_to_json(st.session_state.chat_history)
    speak(f'the time now is {time_now}')

def date_time_find_speak():
    time_set = datetime.datetime.now()
    time_now = time_set.strftime('%I:%M %p')

    date_set = datetime.date.today()
    date_today = date_set.strftime('%d %B %Y')

    website_conversation('', f'The time and date is {time_now} {date_today}')
    st.session_state.chat_history.append({"role": "assistant", "content": f'The time and date is {time_now} {date_today}'})
    save_chat_to_json(st.session_state.chat_history)
    speak(f'The time and date is {time_now} {date_today}')

def date_find_chat():
    date_set = datetime.date.today()
    date_today = date_set.strftime('%d %B %Y')
    website_conversation('', f'The date today is {date_today}')
    st.session_state.chat_history.append({"role": "assistant", "content": f'The date today is {date_today}' })
    save_chat_to_json(st.session_state.chat_history)

def time_find_chat():
    time_set = datetime.datetime.now()
    time_now = time_set.strftime('%I:%M %p')
    website_conversation('', f'the time now is {time_now}')
    st.session_state.chat_history.append({"role": "assistant", "content": f'the time now is {time_now}'})
    save_chat_to_json(st.session_state.chat_history)

def date_time_find_chat():
    time_set = datetime.datetime.now()
    time_now = time_set.strftime('%I:%M %p')

    date_set = datetime.date.today()
    date_today = date_set.strftime('%d %B %Y')

    website_conversation('', f'The time and date is {time_now} {date_today}')
    st.session_state.chat_history.append({"role": "assistant", "content": f'The time and date is {time_now} {date_today}'})
    save_chat_to_json(st.session_state.chat_history)

def play_speak(to_play):
    global proceed
    st.session_state.chat_history.append({"role": "assistant", "content": f'{to_play} played'})
    save_chat_to_json(st.session_state.chat_history)
    website_conversation('', f'playing {to_play}')
    speak(f'playing {to_play}')
    pywhatkit.playonyt(to_play)

def play_chat(to_play):
    st.session_state.chat_history.append({"role": "assistant", "content": f'{to_play} played'})
    save_chat_to_json(st.session_state.chat_history)
    website_conversation('', f'playing {to_play}')
    pywhatkit.playonyt(to_play)

def generate_image_speak(text_for_image, img_description):
    speak(f'Generating Image of {img_description}')
    try:
        client = Client("black-forest-labs/FLUX.1-schnell")

        result = client.predict(
            prompt=text_for_image,
            seed=0,
            randomize_seed=True,
            width=1024,
            height=1024,
            num_inference_steps=4,
            api_name="/infer"
        )
        website_conversation('', result, 'image', 'gradio', f'Image generation of {img_description} completed')
    except:
        hf = open('.venv/Lib/site-packages/API/HUGGING_FACE_API.txt', 'r')
        client = InferenceClient(
            provider="nebius",
            api_key=hf.read(),
        )

        # output is a PIL.Image object
        image_backend = client.text_to_image(
            text_for_image,
            model="black-forest-labs/FLUX.1-schnell",
        )
        website_conversation('', image_backend, 'image', f'Image generation of {img_description} completed')
        speak('Image Generation Completed')

def generate_image_chat(text_for_image, img_description):
    #st.session_state.chat_history.append({"role": "assistant", "content": f'Generating image of {img_description}'})
    try:
        client = Client("black-forest-labs/FLUX.1-schnell")

        result = client.predict(
            prompt=text_for_image,
            seed=0,
            randomize_seed=True,
            width=1024,
            height=1024,
            num_inference_steps=4,
            api_name="/infer"
        )
        website_conversation('', result, 'image', 'gradio', f'Image generation of {img_description} completed')
    except:
        hf = open('.venv/Lib/site-packages/API/HUGGING_FACE_API.txt', 'r')
        client = InferenceClient(
            provider="replicate",
            api_key=hf.read(),
        )

        # output is a PIL.Image object
        image_backend = client.text_to_image(
            text_for_image,
            model="black-forest-labs/FLUX.1-schnell",
        )
        website_conversation('', image_backend, 'image', f'Image generation of {img_description} completed')
    # generated_image = Image.open(io.BytesIO(image_bytes))
    # generated_image.save('Images/generated_image.png')
    # time.sleep(3)
    # pywhatkit.sendwhats_image('+919526573221', r'C:\Users\user\PycharmProjects\AI_VOICE_ASSISTANT\Images\image.png', f'Here is your Image of {img_description}', 20, True, 30)

    # with st.chat_message('assistant', avatar=AI_LOGO):
    #     st.image('Images/generated_image.png', width=350)
    # os.remove('Images/generated_image.png')

def change_voice(gender):
    global voice_preset
    if gender == 'male':
        voice_preset = 'en-US-AndrewNeural'
        st.session_state.chat_history.append({"role": "assistant", "content": 'Voice set to male.'})
        website_conversation('', 'Voice set to male.')
        speak('Voice set to male')
    elif gender == 'female':
        voice_preset = 'en-US-AvaNeural'
        st.session_state.chat_history.append({"role": "assistant", "content": 'Voice set to female.'})
        website_conversation('', 'Voice set to female.')
        speak('Voice set to female')
    else:
        pass



def ask_ai_speak(text_for_ai, save = True):
    groq = open('.venv/Lib/site-packages/API/GROQ_API.txt', 'r')
    global proceed
    output = ''
    client = Groq(api_key=groq.read())

    st.session_state.chat_history.append({"role": "user", "content": text_for_ai})
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=st.session_state.chat_history,
            temperature=1,
            max_tokens=500,
            top_p=0.65,
            stream=True,
            stop=None,
        )
        for chunk in completion:
            print(chunk.choices[0].delta.content or "", end="")
            output += chunk.choices[0].delta.content or ""
    except:
        try:
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=st.session_state.chat_history,
                temperature=1,
                max_tokens=500,
                top_p=0.65,
                stream=True,
                stop=None,
            )
            for chunk in completion:
                print(chunk.choices[0].delta.content or "", end="")
                output += chunk.choices[0].delta.content or ""
        except:
            completion = client.chat.completions.create(
                model="meta-llama/llama-4-maverick-17b-128e-instruct",
                messages=st.session_state.chat_history,
                temperature=1,
                max_tokens=500,
                top_p=0.65,
                stream=True,
                stop=None,
            )
            for chunk in completion:
                print(chunk.choices[0].delta.content or "", end="")
                output += chunk.choices[0].delta.content or ""

    if not save:
        del st.session_state.chat_history[-1]
    st.session_state.chat_history.append({"role": "assistant", "content": output})
    save_chat_to_json(st.session_state.chat_history)
    if '<tool_call>' in output:
        input_string = output.replace('<tool_call>', '').replace('</tool_call>', '').strip()
        data = json.loads(input_string)
        tool_name = data['name']
        tool_description = data["arguments"]["description"]

        if tool_name == 'generate_image':
            generate_image_speak(tool_description, data["arguments"]["description"])
        elif tool_name == 'change_voice':
            if 'female' in tool_description:
                change_voice('female')
            elif 'male' in tool_description:
                change_voice('male')
        elif tool_name == 'play':
            proceed = False
            play_speak(tool_description)
            output = '~break'
        elif tool_name == 'sleep_cutoff':
            proceed = False
            st.session_state.chat_history.append({"role": "assistant", "content": tool_description})
            website_conversation('', tool_description)
            speak(tool_description)
            playsound('Audios/sleep_beep.mp3')
            output = '~break'
        elif tool_name == 'time':
            time_find_speak()
        elif tool_name == 'date':
            date_find_speak()
        elif tool_name == 'time_date':
            date_time_find_speak()
        elif tool_name == 'air_quality_analyze':
            air_quality_analyze_speak()
    return output

def ask_ai_chat(text_for_ai, save = True, for_app = False):
    groq = open('.venv/Lib/site-packages/API/GROQ_API.txt', 'r')
    output = ''
    client = Groq(api_key=groq.read())

    st.session_state.chat_history.append({"role": "user", "content": text_for_ai})
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=st.session_state.chat_history,
            temperature=1,
            max_tokens=500,
            top_p=0.65,
            stream=True,
            stop=None,
        )
        for chunk in completion:
            print(chunk.choices[0].delta.content or "", end="")
            output += chunk.choices[0].delta.content or ""
            # for i in range(7, len(output)):
            #     if i == '>' and output[i - 1] == 'k' and output[i - 2] == 'n':
            #         output = output[i:]
            #         print(output)
    except:
        try:
            completion = client.chat.completions.create(
                model="meta-llama/llama-4-maverick-17b-128e-instruct",
                messages=st.session_state.chat_history,
                temperature=1,
                max_tokens=100,
                top_p=0.65,
                stream=True,
                stop=None,
            )
            for chunk in completion:
                print(chunk.choices[0].delta.content or "", end="")
                output += chunk.choices[0].delta.content or ""
                # for i in range(7, len(output)):
                #     if i == '>' and output[i-1] == 'k' and output[i-2] == 'n':
                #         output = output[i:]
        except:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.chat_history,
                temperature=1,
                max_tokens=500,
                top_p=0.65,
                stream=True,
                stop=None,
            )
            for chunk in completion:
                print(chunk.choices[0].delta.content or "", end="")
                output += chunk.choices[0].delta.content or ""
                # for i in range(7, len(output)):
                #     if i == '>' and output[i-1] == 'k' and output[i-2] == 'n':
                #         output = output[i:]
    if not save:
        del st.session_state.chat_history[-1]
    st.session_state.chat_history.append({"role": "assistant", "content": output})
    save_chat_to_json(st.session_state.chat_history)
    if not for_app:
        if '<tool_call>' in output:
            input_string = output.replace('<tool_call>', '').replace('</tool_call>', '')
            data = json.loads(input_string)
            tool_name = data['name']
            tool_description = data["arguments"]["description"]

            if tool_name == 'generate_image':
                generate_image_chat(tool_description, data["arguments"]["description"])
            elif tool_name == 'sleep_cutoff':
                st.session_state.chat_history.append({"role": "assistant", "content": tool_description})
                website_conversation('', tool_description)
            elif tool_name == 'play':
                play_chat(tool_description)
            elif tool_name == 'time':
                time_find_chat()
            elif tool_name == 'date':
                date_find_chat()
            elif tool_name == 'time_date':
                date_time_find_chat()
            elif tool_name == 'air_quality_analyze':
                air_quality_analyze_chat()


    return output

import threading

def speak(text):
    global voice_preset
    voices = ['en-US-GuyNeural', 'en-US-JennyNeural', 'en-US-AvaMultilingualNeural', 'en-US-AndrewMultilingualNeural',
              'en-US-EmmaMultilingualNeural', 'en-US-BrianMultilingualNeural', 'en-US-AvaNeural', 'en-US-AndrewNeural',
              'en-US-EmmaNeural', 'en-US-BrianNeural', 'en-US-AnaNeural', 'en-US-AriaNeural', 'en-US-ChristopherNeural',
              'en-US-EricNeural', 'en-US-GuyNeural', 'en-US-JennyNeural', 'en-US-MichelleNeural', 'en-US-RogerNeural',
              'en-US-SteffanNeural']
    # 6 7 18

    output_file = "AI_out.mp3"

    async def main():
        communicate = edge_tts.Communicate(text, voice_preset)
        await communicate.save(output_file)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        pass

    playsound('AI_out.mp3')
    os.remove('AI_out.mp3')


def listen_record_transcribe(file_path):
    global proceed
    listener = sr.Recognizer()
    playsound('Audios/start_beep.mp3')
    with sr.Microphone() as source:
        print('Recording Started...')
        audio_data = listener.listen(source)
        print('Recording Completed.')
    with open(file_path, 'wb') as audio_file:
        audio_file.write(audio_data.get_wav_data())

    groq = open('.venv/Lib/site-packages/API/GROQ_API.txt', 'r')
    client = Groq(api_key=groq.read())
    filename = os.path.dirname(__file__) + f"/{file_path}"

    with (open(filename, "rb") as file):
        transcription = client.audio.transcriptions.create(
            file=(filename, file.read()),
            model="whisper-large-v3-turbo",
            temperature=0,
            language="en",
            response_format="verbose_json",
        )
        print(transcription.text)
        print("hello__", proceed)
        if not proceed and not transcription.text.startswith(' Thank you.') and transcription.text != '':
            return transcription.text
        elif not proceed and transcription.text.startswith(' Thank you.') and transcription.text == '':
            return '~break'

def clear_chat_history():
    st.session_state.chat_history = [
        {'role': 'system', 'content': 'You are a friendly assistant'},
        {'role': 'system',
         'content': 'Always keep your replies unique from one another, never repeat again and again if the user is repeating'},
        {'role': 'system',
         'content': 'You are Llama 4 a large AI model created by meta, and was modified by Mohammed Swalih for Sairobss. Remember the full form of sairobss is Swalih Artificial Intelligence Robotic Security System.'},
        {'role': 'system',
         'content': 'Mohammed Swalih is 12th grade student, and the creator SAIROBSS AI. He have won 2nd place in AI and Robotics in the international digital fest that took place at UAE on 2024'},
        {'role': 'system',
         'content': 'Always use json when function call is done: your response should be in this format: <tool_call> {"id": 0, "name": "", "arguments": {"description": ""}} </tool_call>'},
        {'role': 'system',
         'content': 'If the user want to generate an image,you dont have to reply to it, just call the <tool_call> function and make the name "generate_image" and the the arguments as description'},
        {'role': 'system',
         'content': 'call the <tool_call> if the user wants to generate an image and make the name "generate_image" and the the arguments as description, and you do not have to reply to it, just do tool call'},
        {'role': 'system', 'content': '''If the user want to generate an image call <tool_call>
        {"id": 0, "name": "generate_image", "arguments": {"description": the description of the image the user wants to generate}}
        </tool_call>
        '''},
        {'role': 'system',
         'content': 'If the user want to generate an image of the same description again or once more call the <tool_call> function and make the name "generate_image" and the the arguments as description and make the description to a different sentence which conveys the same thing the user want to generate'},
        {'role': 'system',
         'content': 'change the description of the tool call according to you whenever user say to generate the image once more'},
        {'role': 'system',
         'content': 'If the user want to change the voice, call the <tool_call> function and make the name "change_voice" and the the arguments as description and the description as to which gender they want to change the voice "male" or "female"'},
        {'role': 'system',
         'content': 'If the user want to play a music or youtube video call the <tool_call> function and make the name "play" and the the arguments as description and the description as what they wanted to play'},
        {'role': 'system',
         'content': 'If the user says bye to you, call the <tool_call> function and make the name "sleep_cutoff" and make the description as your reply to that bye'},
        {'role': 'system',
         'content': 'If the user want you to analyze the air quality or want to know the statistics of the air quality, call the <tool_call> function and make the name "air_quality_analyze" and make the description as "air_quality_analyze"'},
        {'role': 'system',
         'content': 'If the user want to know the time, call the <tool_call> function and make the name "time" and make the description as "time"'},
        {'role': 'system',
         'content': 'If the user want to know the date, call the <tool_call> function and make the name "date" and make the description as "date"'},
        {'role': 'system',
         'content': 'If the user want to know both time and date, call the <tool_call> function and make the name "time_date" and make the description as "time_date"'},
        {'role': 'system', 'content': 'whenever you give a code in your answer make sure its syntax highlighted'},
        {'role': 'system', 'content': 'Do not call the tool call unnecessarily'},
        {'role': 'system',
         'content': 'If the user want to change the state of a led, call the tool call function and make its name "toggle_led" and its description as to which state the person want to change the led "on" or "off"'},
        {'role': 'system',
         'content': 'if the user want you to write something, write it, and no need to generate images'},
        {'role': 'system', 'content': 'do not generate an image unless the user states it'},
        {'role': 'system',
         'content': 'If i asks if u can here me or not, reply that you can here me by changing the reply as you like'},
        {'role': 'system', 'content': f'''If the user want you to do 2nd degree air quality analysis, You are a smart AI that has just scanned the indoor air using sensors.
You will get three environmental values: TVOC (in ppb), eCO2 (in ppm), and AQI Level (1–5).
Write a short, friendly air quality report based on the sensor readings u got.

Follow these rules:
- Start with a friendly opening like "Air check complete!" or "Scan finished!".
- Use bold headings for each value: **TVOC**, **eCO2**, **AQI Level**.
- After each header, include the value, an emoji for clarity, and a short explanation in 1–2 sentences.
- Add 2–3 bullet-point tips for keeping air quality high.
- End with a friendly summary sentence saying whether it’s safe for long-term stay.
- Do NOT say "based on the given values" or anything that sounds like someone provided the data manually.
- Start like you're actively reporting your own analysis, e.g. "Here's what I found" or "Air check complete!"
- Keep it concise: 2–3 sentences per section (TVOC, eCO2, AQI)
- Use simple language + emojis for clarity (😊, 🟢, ⚠️, 💨, etc.)

Air Quality Reference:

**TVOC (ppb)**  
>6000 = 😵 Bad headaches, nervous effects  
750–6000 = 😫 Headaches, discomfort  
50–750 = 😐 Restless, discomfort
<50 = 😊 Safe

**eCO2 (ppm)**  
>1500 = 🔴 Bad – Indoor air pollution is serious, ventilate now  
1000–1500 = 🟠 Poor – open windows  
800–1000 = 🟡 Okay – could improve  
600–800 = 🟢 Good  
400–600 = 💚 Excellent

**AQI Level (1–5)**  
5 = 🚫 Extremely bad – avoid staying  
4 = ⚠️ Bad – not for long-term  
3 = 🟡 Moderate – needs ventilation  
2 = 🟢 Good – safe for long-term  
1 = 💚 Excellent – perfect


Example:
Air check complete 🎉!

TVOC 📊
The air is filled with high levels of volatile organic compounds, which can cause bad headaches 🤕 and nervous effects 😵, with a value of 6005 ppb 😨. This is not good for your health 🚫!

eCO2 💨
The carbon dioxide levels are okay, but could be improved for better air quality 🌿, with a value of 800 ppm 🟡. Let's try to reduce it 📉!

AQI Level 📊
The overall air quality is bad and not suitable for long-term stay 🚫, with a value of 4 ⚠️. We need to take action 🚨!

To improve the air quality:

Increase ventilation to reduce TVOC levels 💨
Use air purifiers to minimize eCO2 and TVOC 🧹
Avoid strong chemicals and odors to prevent further pollution 🚮
It's not safe for long-term stay due to the high TVOC levels and poor AQI 🤕. Let's work together to improve it 🌈!

Start your report below:
---

        '''}
        ]

    save_chat_to_json(st.session_state.chat_history)


def clear_gallery():
    image_files = os.listdir('Images')
    for file in image_files:
        if 'generated_image' in file:
            os.remove(f'Images/{file}')

def load_past_chat_history_when_change(tab_change):
     global is_tab_change
     is_tab_change = tab_change

def website_conversation(user_input, ai_or_user_output, type_of_inout =  'text', image_generator = 'api', description_img_append = '', load_preceding_chats=True):
    global img_generation_count, chat_disable
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {'role': 'system', 'content': 'You are a friendly assistant'},
            {'role': 'system',
             'content': 'Always keep your replies unique from one another, never repeat again and again if the user is repeating'},
            {'role': 'system',
             'content': 'You are Llama 4 a large ai model created by meta, and was modified by Mohammed Swalih for Sairobss. Remember the full form of sairobss is Swalih Artificial Intelligence Robotic Security System.'},
            {'role': 'system',
             'content': 'Mohammed Swalih is 12th grade student, and the creator SAIROBSS AI. He have won 2nd place in AI and Robotics in the international digital fest that took place at UAE on 2024'},
            {'role': 'system',
             'content': 'Always use json when function call is done: your response should be in this format: <tool_call> {"id": 0, "name": "", "arguments": {"description": ""}} </tool_call>'},
            {'role': 'system',
             'content': 'If the user want to generate an image,you dont have to reply to it, just call the <tool_call> function and make the name "generate_image" and the the arguments as description'},
            {'role': 'system',
             'content': 'call the <tool_call> if the user wants to generate an image and make the name "generate_image" and the the arguments as description, and you do not have to reply to it, just do tool call'},
            {'role': 'system', 'content': '''If the user want to generate an image call <tool_call>
        {"id": 0, "name": "generate_image", "arguments": {"description": the description of the image the user wants to generate}}
        </tool_call>
        '''},
            {'role': 'system',
             'content': 'If the user want to generate an image of the same description again or once more call the <tool_call> function and make the name "generate_image" and the the arguments as description and make the description to a different sentence which conveys the same thing the user want to generate'},
            {'role': 'system',
             'content': 'change the description of the tool call according to you whenever user say to generate the image once more'},
            {'role': 'system',
             'content': 'If the user want to change the voice, call the <tool_call> function and make the name "change_voice" and the the arguments as description and the description as to which gender they want to change the voice "male" or "female"'},
            {'role': 'system',
             'content': 'If the user want to play a music or youtube video call the <tool_call> function and make the name "play" and the the arguments as description and the description as what they wanted to play'},
            {'role': 'system',
             'content': 'If the user says bye to you, call the <tool_call> function and make the name "sleep_cutoff" and make the description as your reply to that bye'},
            {'role': 'system',
             'content': 'If the user want you to analyze the air quality or want to know the statistics of the air quality, call the <tool_call> function and make the name "air_quality_analyze" and make the description as "air_quality_analyze"'},
            {'role': 'system',
             'content': 'If the user want to know the time, call the <tool_call> function and make the name "time" and make the description as "time"'},
            {'role': 'system',
             'content': 'If the user want to know the date, call the <tool_call> function and make the name "date" and make the description as "date"'},
            {'role': 'system',
             'content': 'If the user want to know both time and date, call the <tool_call> function and make the name "time_date" and make the description as "time_date"'},
            {'role': 'system', 'content': 'whenever you give a code in your answer make sure its syntax highlighted'},
            {'role': 'system', 'content': 'Do not call the tool call unnecessarily'},
            {'role': 'system',
             'content': 'If the user want to change the state of a led, call the tool call function and make its name "toggle_led" and its description as to which state the person want to change the led "on" or "off"'},
            {'role': 'system',
             'content': 'if the user want you to write something, write it, and no need to generate images'},
            {'role': 'system', 'content': 'do not generate an image unless the user states it'},
            {'role': 'system',
             'content': 'If i asks if u can here me or not, reply that you can here me by changing the reply as you like'},
            {'role': 'system', 'content': f'''If the user want you to do 2nd degree air quality analysis, You are a smart AI that has just scanned the indoor air using sensors.
You will get three environmental values: TVOC (in ppb), eCO2 (in ppm), and AQI Level (1–5).
Write a short, friendly air quality report based on the sensor readings u got.

Follow these rules:
- Start with a friendly opening like "Air check complete!" or "Scan finished!".
- Use bold headings for each value: **TVOC**, **eCO2**, **AQI Level**.
- After each header, include the value, an emoji for clarity, and a short explanation in 1–2 sentences.
- Add 2–3 bullet-point tips for keeping air quality high.
- End with a friendly summary sentence saying whether it’s safe for long-term stay.
- Do NOT say "based on the given values" or anything that sounds like someone provided the data manually.
- Start like you're actively reporting your own analysis, e.g. "Here's what I found" or "Air check complete!"
- Keep it concise: 2–3 sentences per section (TVOC, eCO2, AQI)
- Use simple language + emojis for clarity (😊, 🟢, ⚠️, 💨, etc.)

Air Quality Reference:

**TVOC (ppb)**  
>6000 = 😵 Bad headaches, nervous effects  
750–6000 = 😫 Headaches, discomfort  
50–750 = 😐 Some discomfort  
<50 = 😊 Safe

**eCO2 (ppm)**  
>1500 = 🔴 Bad – ventilate now  
1000–1500 = 🟠 Poor – open windows  
800–1000 = 🟡 Okay – could improve  
600–800 = 🟢 Good  
400–600 = 💚 Excellent

**AQI Level (1–5)**  
5 = 🚫 Extremely bad – avoid staying  
4 = ⚠️ Bad – not for long-term  
3 = 🟡 Moderate – needs ventilation  
2 = 🟢 Good – safe for long-term  
1 = 💚 Excellent – perfect


Example:
Air check complete 🎉!

TVOC 📊
The air is filled with high levels of volatile organic compounds, which can cause bad headaches 🤕 and nervous effects 😵, with a value of 6005 ppb 😨. This is not good for your health 🚫!

eCO2 💨
The carbon dioxide levels are okay, but could be improved for better air quality 🌿, with a value of 800 ppm 🟡. Let's try to reduce it 📉!

AQI Level 📊
The overall air quality is bad and not suitable for long-term stay 🚫, with a value of 4 ⚠️. We need to take action 🚨!

To improve the air quality:

Increase ventilation to reduce TVOC levels 💨
Use air purifiers to minimize eCO2 and TVOC 🧹
Avoid strong chemicals and odors to prevent further pollution 🚮
It's not safe for long-term stay due to the high TVOC levels and poor AQI 🤕. Let's work together to improve it 🌈!


Start your report below:
---
        '''}
        ]
        #save_chat_to_json(st.session_state.chat_history)
    if load_preceding_chats and ai_or_user_output == '':
        st.session_state.chat_history = load_chat_from_json()
        for message in st.session_state.chat_history:
            if message['role'] == 'assistant':
                avatar = AI_LOGO
                content = message['content']
                if 'tool_call' not in content and 'tool call' not in content:
                    with st.chat_message(message["role"], avatar=avatar):
                        st.markdown(message["content"])

            elif message['role'] == 'user':
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    if user_input != '':
        updated_user_input = user_input
        if '#' in user_input:
            updated_user_input = user_input.replace('#', '\\#')

        if user_input:
            with st.chat_message("user"):
                #st.session_state.chat_history.append({"role": "user", "content": updated_user_input})
                st.markdown(updated_user_input)

    if ai_or_user_output != '' and load_preceding_chats:
        if type_of_inout == 'text':
            with st.chat_message("assistant", avatar=AI_LOGO):
                #st.markdown(ai_or_user_output)
                placeholder = st.empty()
                displayed_text = ""
                for char in ai_or_user_output:
                    displayed_text += char
                    placeholder.markdown(displayed_text)
                    time.sleep(0.007)
            #st.session_state.chat_history.append({"role": "assistant", "content": ai_or_user_output})

        elif type_of_inout == 'image':
            img_generation_count += 1
            if image_generator == 'api':
                generated_image = ai_or_user_output
                generated_image.save(f'Images/generated_image{img_generation_count}.png')
            elif image_generator == 'gradio':
                img_path = ai_or_user_output[0]  # path to the image (usually .webp)
                img_modified = Image.open(img_path)
                img_modified.save(f'Images/generated_image{img_generation_count}.png', format="PNG")
                if os.path.exists(img_path):
                    os.remove(img_path)

            with st.chat_message("assistant", avatar=AI_LOGO):
                try:
                    st.markdown(description_img_append)
                    st.image(f'Images/generated_image{img_generation_count}.png', width=350)
                    pyautogui.hotkey('ctrl', 'end')
                    st.session_state.chat_history.append({"role": "assistant", "content": description_img_append})
                except:
                    pass


def voice_chat():
    global proceed
    playsound('Audios/wake_beep.mp3')
    while proceed:
        user_input = listen_record_transcribe('Audios/user_in.wav', )
        if user_input != '' and not user_input.startswith(' Thank you.'):
            website_conversation(user_input, '', load_preceding_chats=False)
            ai_output = ask_ai_speak(user_input)
            if 'tool_call' not in ai_output and 'tool call' not in ai_output:
                website_conversation('', ai_output)
                speak(ai_output)
