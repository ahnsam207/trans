import streamlit as st
import requests

# Function to perform translation using the Google Translate API
def translate_text(source_text, target_lang):
    try:
        response = requests.get(
            f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={source_text}"
        )
        data = response.json()
        if data and isinstance(data, list) and isinstance(data[0], list):
            return ''.join([item[0] for item in data[0] if item])
        return "Translation failed. Please try again."
    except Exception as e:
        return "Translation failed. Please try again."

# Streamlit page setup
st.set_page_config(page_title="Translation App", layout="centered")
st.title("Translation App")

# Input text area
source_text = st.text_input("텍스트를 입력하세요", "")
target_lang = st.selectbox(
    "목표 언어를 선택하세요",
    options=["en", "ja", "zh", "ko"],
    format_func=lambda x: {
        "en": "🇬🇧 English",
        "ja": "🇯🇵 日本語",
        "zh": "🇨🇳 中文",
        "ko": "🇰🇷 한국어"
    }[x]
)

# Button to trigger translation
if st.button("번역"):
    if source_text:
        with st.spinner("번역 중..."):
            translation = translate_text(source_text, target_lang)
            st.success(translation)
    else:
        st.warning("텍스트를 입력해주세요.")

# Button for speaking the translated text
if st.button("🔊 Speak"):
    if source_text:
        translation = translate_text(source_text, target_lang)
        if translation and translation != "Translation failed. Please try again.":
            # Simple text-to-speech using HTML and JavaScript
            st.markdown(
                f"<audio controls autoplay>"
                f"<source src='https://api.voicerss.org/?key=YOUR_API_KEY&hl={target_lang}&src={translation}' type='audio/mpeg'>"
                f"</audio>",
                unsafe_allow_html=True
            )
        else:
            st.warning("먼저 텍스트를 번역해주세요.")
    else:
        st.warning("먼저 텍스트를 입력해주세요.")