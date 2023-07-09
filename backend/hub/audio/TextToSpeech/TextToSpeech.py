import pyttsx3

# TO BE IMPLEMENTED

class TextToSpeech:
    def __init__(self, hub):
        self.hub = hub
        self.engine = None

    def start(self):
        self.engine = pyttsx3.init()
        self.engine.runAndWait()

    def display_msg(self, msg):
        print("ttsing msg =", msg)
        self.engine.say(msg)
