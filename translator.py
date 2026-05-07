import streamlit as st
from translator import translate

st.set_page_config(
    page_title="AI Translator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      .stApp {
        background: radial-gradient(1200px 600px at 10% -10%, #1f3b73 0%, #0a0f1f 40%, #060912 100%);
        color: #f3f5f7;
      }
      .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 2rem;
      }
      .hero {
        background: linear-gradient(135deg, rgba(67,97,238,0.22), rgba(0,212,255,0.16));
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 20px;
        padding: 1.2rem 1.4rem;
        backdrop-filter: blur(8px);
        margin-bottom: 1rem;
      }
      .card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px;
        padding: 1rem;
      }
      .stTextArea textarea {
        border-radius: 12px;
      }
      .stButton button {
        background: linear-gradient(90deg,#5b8cff,#1ec8ff);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1rem;
        font-weight: 600;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class='hero'>
      <h1 style='margin:0'>🌐 Smart Translator</h1>
      <p style='margin:0.4rem 0 0 0; opacity:0.85'>企业级风格翻译体验：快速、清晰、舒适。</p>
    </div>
    """,
    unsafe_allow_html=True,
)

languages = {
    "自动检测": "auto",
    "中文": "zh",
    "English": "en",
    "日本語": "ja",
    "한국어": "ko",
    "Français": "fr",
    "Deutsch": "de",
    "Español": "es",
    "Português": "pt",
    "Русский": "ru",
    "العربية": "ar",
}

left, right = st.columns(2)
with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    source_label = st.selectbox("源语言", list(languages.keys()), index=0)
    text = st.text_area("输入文本", height=280, placeholder="在此输入需要翻译的内容...")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    target_options = [k for k in languages.keys() if k != "自动检测"]
    target_label = st.selectbox("目标语言", target_options, index=1)
    output_box = st.empty()
    st.markdown("</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 4])
with col1:
    run = st.button("开始翻译", use_container_width=True)

if run:
    if not text.strip():
        st.warning("请输入要翻译的文本。")
    else:
        with st.spinner("翻译中..."):
            try:
                result = translate(text, languages[source_label], languages[target_label])
                output_box.text_area("翻译结果", value=result, height=280)
            except Exception as exc:
                st.error(f"翻译失败：{exc}")
else:
    output_box.text_area("翻译结果", value="", height=280, placeholder="结果会显示在这里")
