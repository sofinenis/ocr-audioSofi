import streamlit as st
import os
import time
import glob
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
from googletrans import Translator

# 🌻 CONFIGURACIÓN GENERAL
st.set_page_config(page_title="🌻 Reconócete Hermana", page_icon="🌻", layout="centered")

# 🌻 ESTILO VISUAL
st.markdown("""
    <style>
        body {
            background-color: #fff8dc;
        }
        .main {
            background-color: #fffbea;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0px 0px 15px rgba(245, 200, 30, 0.4);
        }
        h1, h2, h3 {
            color: #e1a72a;
            text-align: center;
            font-family: 'Comic Sans MS', cursive;
        }
        .stButton>button {
            background-color: #ffd54f;
            color: #4a3000;
            border-radius: 10px;
            border: 2px solid #e1a72a;
            font-weight: bold;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #ffeb3b;
            transform: scale(1.05);
        }
        .stTextInput>div>div>input, .stTextArea>div>textarea {
            background-color: #fff8b0;
            border-radius: 10px;
            border: 2px solid #f1c40f;
            color: #4a3000;
        }
        .stSelectbox>div>div {
            background-color: #fff8d6;
        }
        .stSidebar {
            background-color: #fff7d6;
        }
        .uploadedFile {
            border: 2px solid #e1a72a;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# 🌻 FUNCIONES AUXILIARES
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("🗑️ Deleted ", f)

remove_files(7)

def text_to_speech(input_language, output_language, text, tld):
    translator = Translator()
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    try:
        my_file_name = text[0:20].strip().replace(" ", "_")
    except:
        my_file_name = "audio"
    os.makedirs("temp", exist_ok=True)
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text

# 🌻 INTERFAZ PRINCIPAL
st.title("🌻 Reconócete Hermana 🌞")
st.subheader("💛 Muéstrame algo y deja que florezca en sonido 🌼")

# 🌼 OPCIÓN DE CÁMARA
cam_ = st.checkbox("📸 Usar Cámara para capturar imagen")

if cam_:
    img_file_buffer = st.camera_input("🌻 Toma una foto con tu cámara")
else:
    img_file_buffer = None

# 🌻 SIDEBAR - PARÁMETROS
with st.sidebar:
    st.header("🌻 Panel de Opciones 🌼")
    filtro = st.radio("🌞 Aplicar filtro de inversión (para texto oscuro):", ('Sí', 'No'))
    st.markdown("---")
    st.subheader("🎧 Parámetros de Traducción y Voz")

    translator = Translator()
    
    in_lang = st.selectbox(
        "🌻 Selecciona el lenguaje de entrada:",
        ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"),
    )
    lang_dict = {"Inglés": "en", "Español": "es", "Bengali": "bn", "Coreano": "ko", "Mandarín": "zh-cn", "Japonés": "ja"}
    input_language = lang_dict[in_lang]

    out_lang = st.selectbox(
        "🌼 Selecciona el lenguaje de salida:",
        ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"),
    )
    output_language = lang_dict[out_lang]

    english_accent = st.selectbox(
        "☀️ Selecciona el acento:",
        ("Default", "India", "Reino Unido", "Estados Unidos", "Canadá", "Australia", "Irlanda", "Sudáfrica"),
    )
    accent_tld = {
        "Default": "com",
        "India": "co.in",
        "Reino Unido": "co.uk",
        "Estados Unidos": "com",
        "Canadá": "ca",
        "Australia": "com.au",
        "Irlanda": "ie",
        "Sudáfrica": "co.za",
    }
    tld = accent_tld[english_accent]

    display_output_text = st.checkbox("🌻 Mostrar texto traducido")

# 🌻 SUBIDA DE IMAGEN DESDE ARCHIVO
bg_image = st.file_uploader("🌻 O carga una imagen desde tu dispositivo:", type=["png", "jpg", "jpeg"])
text = ""

if bg_image is not None:
    st.image(bg_image, caption="🌞 Imagen cargada correctamente 🌻", use_container_width=True)
    bytes_data = bg_image.read()
    np_img = np.frombuffer(bytes_data, np.uint8)
    img_cv = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    st.success("🌼 Texto detectado en la imagen:")
    st.write(text)

# 🌻 PROCESAMIENTO DE IMAGEN CAPTURADA POR CÁMARA
elif img_file_buffer is not None:
    st.info("🌻 Procesando imagen capturada... ☀️")
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if filtro == 'Sí':
        cv2_img = cv2.bitwise_not(cv2_img)
        st.caption("🌼 Filtro aplicado (inversión de color) 🌻")

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    st.image(img_rgb, caption="🌞 Imagen procesada", use_container_width=True)
    text = pytesseract.image_to_string(img_rgb)
    st.success("🌻 Texto extraído de la foto:")
    st.write(text)

else:
    st.info("🌻 Esperando una imagen... puedes tomar una foto o subir un archivo 🌼")

# 🌻 BOTÓN DE CONVERSIÓN A AUDIO
if text.strip() != "":
    if st.button("🎶 Convertir texto a audio 🌻"):
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.success("🌻 ¡Tu audio floreció con éxito! 🌞")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        if display_output_text:
            st.markdown("## 🌼 Texto traducido:")
            st.write(f"💬 {output_text}")
else:
    st.warning("🌻 Aún no hay texto para convertir. Sube o captura una imagen con texto 🌞")

