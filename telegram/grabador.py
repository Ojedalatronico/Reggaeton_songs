import os
from gtts import gTTS

def audio(envio, chat):
    speech = gTTS(text = envio, lang = "es-es", slow =False)
    speech.save("texto.ogg")
    chat.send_audio(
        audio=open("texto.ogg", "rb")
    )
    os.unlink("texto.ogg")