import os
import time

import pyautogui
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import pywhatkit
import datetime
import plotly.graph_objects as go
import random
import requests
from streamlit_lottie import st_lottie
from firebase_admin import db
from pynput.keyboard import Controller, Key
from ai_functions import website_conversation, ask_ai_chat, is_tab_change, load_past_chat_history_when_change, \
    clear_chat_history, chat_disable, clear_gallery, voice_chat, change_proceed_state, proceed, \
    listen_record_transcribe, ask_ai_speak, speak, check_message

AI_LOGO= Image.open('Images/SAIROBSS_LOGO_NEW_LOGO.png')
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_animation = load_lottie_url('https://lottie.host/d35452c9-3ce8-4999-946f-22bbe19f971b/srXtdkfEkF.json')
def redirect_check_message(event):
    check_message(event)
change_proceed_state(False)
st.set_page_config(
        page_title="SAIROBSS AI",
        page_icon=AI_LOGO,
        layout="wide",
    )

with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=['Home','Dashboard','AI images', 'Chat', 'Voice chat', 'File AI', 'Vision AI'],
        menu_icon='chat-square-dots',
        icons=['house', 'speedometer2', 'images', 'chat-right-text', 'mic', 'file-earmark-break', 'eye'],
        default_index=0,
)


voice_preset = 'en-US-AndrewNeural'


if selected == 'Home':
    st.write('##')
    load_past_chat_history_when_change(True)
    with st.container():
        left_column, right_column = st.columns([4,1])
    with left_column:
        st.title('Welcome to SAIROBSS AI')
        st.text('Powered by Llama 4 and Whisper Large')
    with right_column:
        st.image('Images/SAILogo.png', width=150, output_format='PNG')
    st_lottie(lottie_animation,height=300)
    st.header('Overview on SAIROBSS AI')
    st.html("<p>SAIROBSS AI is an AI chat and voice bot powered by Llama 4 and Whisper large exclusively modified by Mohammed Swalih for SAIROBSS (SWALIH ARTIFICIAL INTELLIGENCE ROBOTIC SECURITY SYSTEM). Now when technological advancement in AI is at its peak, a robot without an AI influence is powerless</p>")

elif selected == 'Dashboard':
    load_past_chat_history_when_change(True)
    st.title("⛅ Environmental Dashboard")
    if st.button('START ENVIRONMENT ANALYSES'):

        st.markdown("""
                        <style>
                            .stButton > Button {
                                visibility: hidden; 
                                }
                        <style>
                    """, unsafe_allow_html=True)
    # Layout
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        temp_placeholder = col1.empty()
        humidity_placeholder = col2.empty()
        voc_placeholder = col3.empty()
        aiq_placeholder = col4.empty()

        # AIQ mapping
        aiq_map = {
            1: "😄 Excellent",
            2: "🙂 Good",
            3: "😐 Moderate",
            4: "😷 Poor",
            5: "☠️ Very Poor"
        }

        # Main loop
        for i in range(100):
            temp = i % 101
            humidity = random.randint(30, 90)
            voc = random.randint(0, 300)
            eco2 = random.randint(0, 1000)
            aiq = random.randint(1, 5)

            # --- Temperature Gauge ---
            r = int(255 * (temp / 100))
            g = int(102 * (1 - (temp / 100)))
            b = int(255 * (1 - (temp / 100)))

            temp_fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=temp,
                title={'text': "🌡️ Temperature (°C)", 'font': {'size': 20}},
                number={'font': {'size': 20}},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': f'rgba({r},{g},{b},1)'},
                    'steps': [{'range': [0, 100], 'color': 'rgba(255,255,255,0)'}]
                }
            ))
            temp_fig.update_layout(height=170, margin=dict(t=50, b=15, l=15, r=15))
            temp_placeholder.plotly_chart(temp_fig, width="stretch")

            # --- Humidity Wave ---
            humidity_placeholder.markdown(f"""
            <style>
            @keyframes waveAnimation {{
              0% {{ transform: translateX(0); }}
              100% {{ transform: translateX(-50%); }}
            }}
            .wave-container {{
              position: relative;
              width: 100%;
              height: 100px;
              background-color: #dedcdc;
              border-radius: 15px;
              overflow: hidden;
              box-shadow: inset 0 0 10px #000;
            }}
            .wave-fill {{
              position: absolute;
              bottom: 0;
              width: 200%;
              height: {humidity}%;
              background-color: transparent;
              display: flex;
              animation: waveAnimation 4s linear infinite;
            }}
            .wave-fill svg {{
              width: 50%;
              height: 100%;
            }}
            .wave-text {{
              position: absolute;
              top: 0;
              left: 0;
              width: 100%;
              height: 100%;
              color: white;
              font-size: 24px;
              font-weight: bold;
              display: flex;
              align-items: center;
              justify-content: center;
              text-shadow: 1px 1px 2px #000;
              z-index: 2;
            }}
            </style>
            <div style="margin-bottom: 10px;">
              <h4 style="color: black; margin: 0;">💧 Humidity</h4>
            </div>
            <div class="wave-container" style="margin-bottom: 20px;">
              <div class="wave-fill">
                <svg viewBox="0 0 1200 100" preserveAspectRatio="none">
                  <path d="M0,30 C300,80 900,-20 1200,30 V100 H0 Z" fill="#42A5F5" />
                </svg>
                <svg viewBox="0 0 1200 100" preserveAspectRatio="none">
                  <path d="M0,30 C300,80 900,-20 1200,30 V100 H0 Z" fill="#42A5F5" />
                </svg>
              </div>
              <div class="wave-text">{humidity}%</div>
            </div>
            """, unsafe_allow_html=True)

            # --- VOC & eCO2 as Bars ---
            voc_placeholder.markdown(f"""
            <style>
            .voc-eco2-box {{
              background-color: #ffffff;
              border-radius: 15px;
              padding: 20px;
              position: relative;
              overflow: hidden;
              height: 160px;
              color: #333;
              text-align: center;
              box-shadow: 0 0 10px #ccc;
              font-family: 'Segoe UI', sans-serif;
            }}

            .bubble {{
              position: absolute;
              border-radius: 50%;
              background: rgba(0, 128, 0, 0.6);  /* CO₂ - grey smoky */
              bottom: -40px;
              animation: rise 6s infinite ease-in;
            }}

            .ring {{
              position: absolute;
              width: 12px;
              height: 12px;
              border: 2px solid rgba(250, 156, 28, 0.5);  /* VOC - CornflowerBlue */
              border-radius: 50%;
              animation: pulse 3s ease-out infinite;
            }}

            @keyframes rise {{
              0% {{ transform: translateY(0); opacity: 0; }}
              50% {{ opacity: 1; }}
              100% {{ transform: translateY(-160px); opacity: 0; }}
            }}

            @keyframes pulse {{
              0% {{
                transform: scale(0.6);
                opacity: 0.7;
              }}
              70% {{
                transform: scale(2.5);
                opacity: 0.1;
              }}
              100% {{
                transform: scale(0.6);
                opacity: 0;
              }}
            }}

            .label {{
              font-size: 18px;
              font-weight: 600;
              z-index: 2;
              position: relative;
            }}

            .value {{
              font-size: 22px;
              font-weight: bold;
              z-index: 2;
              position: relative;
            }}

            .values-container {{
              display: flex;
              justify-content: space-around;
              margin-top: 20px;
              z-index: 2;
              position: relative;
            }}
            </style>

            <div class="voc-eco2-box">
              {"".join([f'<div class="ring" style="top:{i * 12}px; left:{i * 9}%; animation-delay: {i * 0.4}s;"></div>' for i in range(10)])}
              {"".join([f'<div class="bubble" style="width:{size}px; height:{size}px; left:{i * 10}%; animation-delay: {i}s;"></div>' for i, size in enumerate(range(10, 30, 4))])}

              <div class="values-container">
                <div>
                  <div class="label">VOC</div>
                  <div class="value">{voc} ppb</div>
                </div>
                <div>
                  <div class="label">eCO₂</div>
                  <div class="value">{eco2} ppm</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # --- AIQ ---
            # --- AIQ ---
            aiq_label = aiq_map[aiq]
            if aiq <= 2:
                bg = '#d4edda'
                pulse_color = '#4CAF50'  # Green
            elif aiq == 3:
                bg = '#fff3cd'
                pulse_color = '#FFC107'  # Yellow
            else:
                bg = '#f8d7da'
                pulse_color = '#F44336'  # Red

            aiq_placeholder.markdown(f"""
                        <style>
                        @keyframes aiqPulse {{
                            0% {{
                                box-shadow: 0 0 0 0 {pulse_color};
                            }}
                            70% {{
                                box-shadow: 0 0 15px 15px rgba(0,0,0,0);
                            }}
                            100% {{
                                box-shadow: 0 0 0 0 rgba(0,0,0,0);
                            }}
                        }}

                        .aiq-unique {{
                            font-size: 40px;
                            text-align: center;
                            padding: 20px;
                            border-radius: 15px;
                            background-color: {bg};
                            color: black;
                            animation: aiqPulse 2s infinite;
                            transition: all 0.3s ease-in-out;
                        }}
                        </style>

                        <div class="aiq-unique">
                            <strong>AIQ: {aiq}</strong><br>{aiq_label}
                        </div>
                        """, unsafe_allow_html=True)

            # 👇 Slow down loop to reduce flicker
            time.sleep(3)

elif selected == 'Chat':
    st.write('##')
    if st.button('Clear history'):
        clear_chat_history()
    user_chat_input = st.chat_input("Message S'AI", key='message_ai_input', disabled=chat_disable)
    if is_tab_change:
        website_conversation('', '')
        load_past_chat_history_when_change(False)
    if user_chat_input is not None:
        website_conversation(user_chat_input, '')
        ai_output = ask_ai_chat(user_chat_input)
        if 'tool_call' not in ai_output and 'tool call' not in ai_output:
            website_conversation('', ai_output)

elif selected == 'Voice chat':
    load_past_chat_history_when_change(True)
    st.write('##')
    st.write('##')
    st.write('##')
    if 'button_pressed' not in st.session_state:
        print('Inside')
        st.session_state.button_pressed = False

    print(st.session_state.button_pressed)

    print(st.session_state.button_pressed)
    pressed = st.button('Start Speaking...' if not st.session_state.button_pressed else 'End Voice chat')
    if pressed:
        st.session_state.button_pressed = not st.session_state.button_pressed
        if not st.session_state.button_pressed:
            change_proceed_state(False)
        elif st.session_state.button_pressed:
            change_proceed_state(True)


    print(st.session_state.button_pressed)
    if is_tab_change:
        website_conversation('', '')
    while proceed:
        print('proceed: ',proceed)
        user_input = listen_record_transcribe('Audios/user_in.wav')
        if user_input is not None and not user_input == '~break':
            website_conversation(user_input, '', load_preceding_chats=False)
            pyautogui.hotkey('ctrl', 'end')
            ai_output = ask_ai_speak(user_input)
            if ai_output == '~break':
                st.session_state.button_pressed = False
                break
            if 'tool_call' not in ai_output and 'tool call' not in ai_output:
                website_conversation('', ai_output)
                pyautogui.hotkey('ctrl', 'end')
                speak(ai_output)
        elif user_input == '~break':
            st.session_state.button_pressed = False
            break
    st.markdown("""
                <style>
                    .stButton > Button {
                        background: linear-gradient(to right, rgb(45, 100, 245), rgb(255, 47, 154));
                        height: 50px;
                        width: 500px;
                        margin-left: 150px;
                        padding: 20px;
                        
                    }
                    .stButton > Button:hover {
                        background: linear-gradient(to right, rgb(35, 90, 235), rgb(245, 37, 144));
                    }
                    .stButton p {
                        font-size: 20px;
                        color: white
                    }
                </style>
                """, unsafe_allow_html=True)
elif selected == 'AI images':
    load_past_chat_history_when_change(True)
    if st.button('Clear gallery'):
        clear_gallery()
    images_file = os.listdir('Images')
    generated_images = []
    for image in images_file:
        if 'generated_image' in image:
            generated_images.append(f'Images/{image}')
    generated_images_group = []
    for i in range(0, len(generated_images), 4):
        generated_images_group.append(generated_images[i:i+4])

    for group in generated_images_group:
        cols = st.columns(4)
        for i, image_file in enumerate(group):
            cols[i].image(image_file)


if selected == 'Vision AI':
    col1, col2 = st.columns([7, 1])

    with col1:
        user_message = st.chat_input("Type a message...")

    with col2:
        if st.button('', icon=":material/attach_file:"):
            pass
        # uploaded_file = st.file_uploader(
        #     "📎",
        #     type=["png", "jpg", "jpeg"],
        #     label_visibility="collapsed"
        # )

if selected == 'File AI':
    st.title("Chat with File Upload")

    uploaded_file = st.file_uploader(
        "📎 Attach an image or file",
        type=["png", "jpg", "jpeg", "pdf", "txt"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")
        user_input_file = st.chat_input('Ask about file', key='message_ai_input_file', disabled=chat_disable)

        if uploaded_file.type.startswith("image"):
            st.image(uploaded_file, caption=uploaded_file.name)
