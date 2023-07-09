import os

import speech_recognition as sr


class SpeechToText:
    def __init__(self, hub):
        print("initiating speechtotext")
        self.hub = hub
        self.enabled = False
        self.azure_key = os.getenv('AZURE_SPEECH_KEY')

    def start(self):
        if not self.enabled:
            print("stt not enabled- exiting now")
            return
        print("starting stt...")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("adjusting for ambient noise")
            r.adjust_for_ambient_noise(source, duration=5)

            if self.enabled:
                print("listening for stt...")
                audio = r.listen(source, timeout=5, phrase_time_limit=30)
                text, score = r.recognize_azure(audio, key=self.azure_key, location='centralus')
                text = text.lower()

                print("transcribed STT:", text, "with score =", score)

                # checks that message was directed towards jade
                if 'jade' in text:
                    # doing it synchronously for now- ensures no more than one message is sent in STT at once. also too
                    # lazy to deal with threading issues
                    msg = text[text.index('jade') + 4:]
                    self.hub.receive_msg(msg)
                    self.hub.gui_display_sent_message(msg)
                else:
                    print("keyword 'jade' not used, so message ignored")

        print("exiting speech to text...")
        self.enabled = False
        self.hub.disable_stt()

    def setEnabled(self, enabled):
        print("switching enabled state from", self.enabled, "to", enabled)
        if enabled != self.enabled:
            self.enabled = enabled
            if self.enabled:
                self.start()

    def stop(self):
        pass
