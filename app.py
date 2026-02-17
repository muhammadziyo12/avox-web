import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- SOZLAMALAR ---
st.set_page_config(page_title="AVOX AI", page_icon="🤖", layout="wide")

# API Kalitni shu yerga qo'y yoki Streamlit Secretlariga yoz
# Xavfsizlik uchun bu yerga to'g'ridan-to'g'ri yozish maslahat berilmaydi,
# lekin test qilish uchun "YOUR_API_KEY" o'rniga o'z kalitingni qo'y.
api_key = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else "YOUR_GEMINI_API_KEY_HERE"

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- SAYT DIZAYNI ---
st.title("🤖 AVOX AI // MOBILE EDITION")
st.write("Salom Senpai! Men sening cho'ntak yordamchingman.")

# Chat tarixi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Avvalgi xabarlarni chiqarish
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 1. KAMERA (VISION) ---
with st.expander("📸 KO'ZNI OCHISH (Vision)"):
    img_file_buffer = st.camera_input("Rasmga oling")

    if img_file_buffer is not None:
        # Rasmni ochamiz
        image = Image.open(img_file_buffer)
        
        # AI ga yuboramiz
        with st.spinner("Avox ko'ryapti..."):
            prompt = "Sen Avoxsan. Rasmdagi narsani qisqa, hazil bilan va do'stona tushuntirib ber (Ingliz yoki O'zbek tilida)."
            response = model.generate_content([prompt, image])
            
            st.success("Tahlil tugadi!")
            st.write(response.text)
            
            # Tarixga qo'shish
            st.session_state.messages.append({"role": "assistant", "content": f"📸 Vision: {response.text}"})

# --- 2. CHAT (TEXT) ---
prompt = st.chat_input("Avoxga yozing...")

if prompt:
    # Senpai yozgani
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Avox javobi
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # AI so'rovi
        chat = model.start_chat(history=[])
        response = chat.send_message(f"Sen Avoxsan. Hazilkash va aqlli yordamchi. Savol: {prompt}")
        
        full_response = response.text
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
