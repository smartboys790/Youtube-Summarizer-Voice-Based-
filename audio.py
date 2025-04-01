from gtts import gTTS

#Test to speech


def speech(summary):
    text= summary
    tts= gTTS(text, lang='en')
    file= tts.save('static/summary.mp3')
    return file
