import streamlit as st
import random
import time
from datetime import datetime, timedelta
import openai
from uma_responses import uma_responses

# -------------------------------
# 页面设置
# -------------------------------
st.set_page_config(
    page_title="我是Uma",
    page_icon="🐢",
    layout="centered"
)

# 背景和头像
avatar_image = "avatar.png"
background_image = "background.png"

st.markdown(f"""
    <style>
    .stApp {{
        background: url({background_image});
        background-size: cover;
    }}
    .chat-bubble {{
        background-color: #fff;
        color: #000;
        border-radius: 5px;
        padding: 8px 12px;
        margin: 5px 0;
        max-width: 70%;
    }}
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# 页面内容
# -------------------------------
st.title("我是Uma，如果你无聊就和我一起推石头吧")
st.subheader("乌龟…. \n乌呃.. \n乌玛！")

# -------------------------------
# OpenAI API Key
# -------------------------------
# 方式1：st.secrets["OPENAI_API_KEY"]
# 方式2：直接填 'sk-xxxx'
openai.api_key = st.secrets["OPENAI_API_KEY"]

# -------------------------------
# 聊天逻辑
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# 对话开始时间
if "start_time" not in st.session_state:
    st.session_state.start_time = datetime.now()

# 限制20分钟对话
def is_time_up():
    return datetime.now() - st.session_state.start_time > timedelta(minutes=20)

# 用户输入
user_input = st.text_input("你想对Uma说：")

if user_input:
    # 保存用户信息
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 50% 词库，50% OpenAI
    use_api = random.random() < 0.5

    if use_api:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是Uma，一只存在主义小龟，只会说简短、冷淡、直接的回答，性格疯癫但高冷。"},
                    *st.session_state.messages
                ],
                max_tokens=2000
            )
            uma_reply = response.choices[0].message.content.strip()
        except Exception as e:
            uma_reply = random.choice(uma_responses)
    else:
        uma_reply = random.choice(uma_responses)

    # 添加Uma回答
    st.session_state.messages.append({"role": "Uma", "content": uma_reply})

# 显示聊天记录
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-bubble" style="background-color:#eee; text-align:right;">你：{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble">Uma：{msg["content"]}</div>', unsafe_allow_html=True)

# 超过20分钟结束
if is_time_up():
    st.info("Uma：时间已到，我要休息了。")
    st.session_state.messages = []
    st.session_state.start_time = datetime.now()