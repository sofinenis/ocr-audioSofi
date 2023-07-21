from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

st.title("Interfaces Multimodales Audio y Texto")

st.write("Interfaz de texto a Audio")
text = st.text_input("Que decir?")

tts_button = Button(label="Decirlo", width=100)

tts_button.js_on_event("button_click", CustomJS(code=f"""
    var u = new SpeechSynthesisUtterance();
    u.text = "{text}";
    u.lang = 'es-es';   

    speechSynthesis.speak(u);
    """))

st.bokeh_chart(tts_button)
