import uuid
import openai
import streamlit as st
from streamlit_chat_media import message

openai.api_key = '[OPENAI_API_KEY]'
IMAGE_COUNT = 3
IMAGE_SIZE = '256x256'

st.set_page_config(page_title="Image generation Chat", page_icon="🎨")
st.markdown("# Welcome to Image generation Chat")
st.sidebar.header("Instruction")
st.sidebar.write("You have to type your prompt and wait for the awesome images")

if 'chat' not in st.session_state:
    st.session_state['chat'] = []

def submit():
    user_input = st.session_state.input
    if user_input:
        user_msg = { 
            'message': f'{user_input}', 
            'type': 'user', 
            'id': f'{uuid.uuid4().hex}' }
        st.session_state.chat.append(user_msg)

        res = generate_images(user_input)
        if res:
            div = '<div>{}</div>'
            imgs = ''
            for im in res['data']:
                imgs = imgs + '<img src="{}" height="150" width="150" />'.format(im['url'])
            
            generated_msg = { 
                'message': f'{div.format(imgs)}', 
                'type': 'generated', 
                'id': f'{uuid.uuid4().hex}' }
            st.session_state.chat.append(generated_msg)

def generate_images(prompt):
  response = openai.Image.create(prompt=prompt, n=IMAGE_COUNT, size=IMAGE_SIZE)
  return response

question = 'anime brunette girl with green eyes'
st.text_input(label = 'Prompt', value = question, key = "input", on_change=submit)

if st.session_state['chat']:
    for msg in reversed(st.session_state['chat']):
        if msg["type"] == 'generated':
            message(msg['message'], allow_html=True, avatar_style = 'icons', key=str(msg['id']))
        else:
            message(msg['message'], avatar_style = 'lorelei-neutral',is_user=True, key=str(msg['id']))




