import streamlit as st
import random

# ---- Uma 头像 URL ----
uma_avatar_url = "https://i.imgur.com/your_avatar.png"  # 替换成你的头像链接

# ---- 语言选择 ----
lang = st.radio("选择语言 / Choose Language", ("中文", "English"))

# ---- Uma 词库 200+ ----
uma_words_cn = [
    "去","不去","好看","不好看","不赖","永远","没兴趣","算了","ok","yes","no",
    "冷淡","淡定","无所谓","看着你了","不理你","睡了","醒了","懒","存在主义",
    "要么要么","随便","好吧","不行","yes or no","搞什么","随它去","不想说",
    "滚石无定","荒诞","疯","冷","拽","认真？","嗯","哈","…","……",
    "看着","走吧","留下","不要","去死","安静","明白","不懂","随意","没问题","行",
    "懒得理","有趣吗","不聊","继续？","随它去吧","好玩？","没关系","算你狠",
    "搞定","走开","哈哈","奇怪","无聊","困","醒","别理我","冷眼旁观",
    "存在即荒诞","看你表演","随缘","不搭理","嗯哼","继续","结束","烦吗","okok",
    "去吧","不去吧","随意吧","试试","不试","也行","别问了","随你"
    # 可以继续补全至 200+
]

uma_words_en = [
    "go","not go","looks good","not good","not bad","not bad","forever","no interest","forget it","ok","yes","no",
    "cold","calm","whatever","looking at you","ignoring you","sleep","awake","lazy","existential",
    "either or","whatever","fine","no","yes or no","what","let it be","don't say",
    "rolling stone","absurd","crazy","cold","arrogant","serious?","hmm","ha","...","……",
    "watching","go","stay","don't","go die","quiet","understand","don't know","whatever","no problem","ok",
    "lazy","fun?","don't chat","continue?","let it be","fun?","no problem","well done",
    "done","go away","ha ha","strange","boring","sleepy","awake","ignore me","cold stare",
    "existence is absurd","watch your show","whatever","ignore","hmm","continue","end","annoying?","okok",
    "go on","not go","whatever","try","not try","fine","stop asking","your choice"
]

# ---- 唯一特殊西西弗名言 ----
special_quote_cn = "西西弗说：我们都是永远在推石头的人，而我是永远在推石头的龟。"
special_quote_en = "Sisyphus says: We are all forever pushing our boulders. And I am the turtle forever pushing my boulder."

# ---- 其他幽默名言（普通版，不加“西西弗说”） ----
quotes_cn = [
    "荒诞即自由","努力本身就是意义","每天都是新的石头滚下山","无望不等于无趣"
]
quotes_en = [
    "Absurdity is freedom","Effort itself is the meaning","Every day brings a new boulder rolling down","Hopelessness is not boredom"
]

# ---- Uma 聊天逻辑 ----
def uma_reply(user_input, lang):
    user_input = user_input.lower().strip()
    
    # 5% 概率输出幽默名言
    if random.random() < 0.05:
        if random.random() < 0.2:  # 20% 概率触发唯一特殊名言
            return special_quote_cn if lang == "中文" else special_quote_en
        else:
            return random.choice(quotes_cn if lang == "中文" else quotes_en)

    # yes/no 关键字逻辑
    yes_keywords_cn = ["出去","玩","穿","喜欢","吃","喝","看","去吗","ok"]
    no_keywords_cn = ["不","不要","不想","讨厌","累","烦","不行","算了","别"]
    yes_keywords_en = ["go","play","wear","like","eat","drink","see","ok"]
    no_keywords_en = ["no","not","don't","hate","tired","bother","stop"]

    yes_keywords = yes_keywords_cn if lang=="中文" else yes_keywords_en
    no_keywords = no_keywords_cn if lang=="中文" else no_keywords_en

    word_bank = uma_words_cn if lang=="中文" else uma_words_en

    if any(word in user_input for word in yes_keywords):
        return "去" if lang=="中文" else "go"
    elif any(word in user_input for word in no_keywords):
        return "不去" if lang=="中文" else "not go"

    return random.choice(word_bank)

# ---- Streamlit Web App ----
st.set_page_config(page_title="Uma 聊天", page_icon="🐢")

st.title("🐢 Uma 聊天 Web App")
st.write("和你的存在主义小龟 Uma 对话！冷淡、荒诞、幽默风格。")

if 'history' not in st.session_state:
    st.session_state.history = []

# 用户输入
user_input = st.text_input("你：" if lang=="中文" else "You:")

if user_input:
    reply = uma_reply(user_input, lang)
    st.session_state.history.append(("你" if lang=="中文" else "You") + ": " + user_input)
    st.session_state.history.append(("Uma" if lang=="中文" else "Uma") + ": " + reply)

# 显示聊天记录
for msg in st.session_state.history:
    if msg.startswith("你:") or msg.startswith("You:"):
        st.markdown(f"<p style='text-align: right; color: blue;'>{msg}</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='text-align: left; color: green;'>{msg}</p>", unsafe_allow_html=True)

# 显示头像
st.image(uma_avatar_url, width=100)