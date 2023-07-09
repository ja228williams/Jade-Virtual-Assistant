import threading
import traceback

from hub.GUI.GUI import GUI
from apps.MusicApp.MusicApp import MusicApp
from hub.audio.SpeechToText.SpeechToText import SpeechToText
from hub.audio.TextToSpeech.TextToSpeech import TextToSpeech
from hub.parser.Parser import Parser


# Hub class
class Hub:
    def __init__(self):
        """
        Initializes Hub and connected components.
        """
        print("initializing hub...")

        # map string representation of developed app to (app_class, app instance), where app instance is None if it
        # has not been created
        self.apps = {'music': [MusicApp, None]}

        # state identification- if not None, message should be directed to app specified by self.responding as a
        # response
        self.responding = None

        # create all of connected components
        self.parser = Parser(self)
        self.text_to_speech = TextToSpeech(self)
        self.speech_to_text = SpeechToText(self)
        self.gui = GUI(self)

        # threads defined as class-wide fields for reference
        self.gui_thread = None
        self.stt_thread = None

    def start(self):
        """
        Enables listening for and processing input.
        """
        print("starting hub...")

        self.gui_thread = threading.Thread(target=lambda: self.gui.start())
        self.stt_thread = threading.Thread(target=lambda: self.speech_to_text.start())
        self.text_to_speech.start()

        self.gui_thread.start()
        print("gui thread started...")
        self.stt_thread.start()
        print("stt thread started...")

        self.gui_thread.join()
        self.stt_thread.join()

    def end_program(self):
        """
        Shuts down necessary running components.
        # TO-DO:
            - figure out how to quit threads for GUI and STT
        """
        print('quitting')
        quit(0)

    def receive_msg(self, msg):
        """
        Processes message sent to hub.

        :param msg: raw string message to be processed
        """
        # msg = "music Play Sun Goes Down by Lil Nas X"

        print("received message '" + msg + "' at hub")

        try:
            # echo message for now
            self.display_msg(msg)

            app = None

            # check if we're starting an app
            words = msg.split()
            for word in words:
                if word in self.apps:
                    # we've found the right app to use
                    app = word
                    break

            if not app:
                # REMOVE LATER
                app = "music"

                # correct behavior to use (unless i decide to add default option)
                # raise Exception("No app identified.")

            # initialize and start app, if necessary
            if not self.apps[app][1]:
                self.display_msg("initializing " + app + "...")
                self.initialize_app(app)
                # self.apps[app][1] = self.apps[app][0](app, self)
                # self.apps[app][1].start()

            # send remainder of message to parser
            # ADD THIS BACK IN LATER- IGNORING NOW FOR TESTING PURPOSES
            new_msg = ' '.join(words[words.index(app) + 1:])
            print("new message:", new_msg)
            resp = self.parser.parse(new_msg, app)

            # forward response determined by parser back to user
            self.display_msg(resp)

        except Exception as e:
            print("Could not process message: ", e)
            print("Traceback:", traceback.format_exc())
            self.display_msg("Failed to process message.")

    def display_msg(self, msg):
        """
        Forwards msg to GUI and text-to-speech for display

        # TO-DO:
            - exception handling

        :param msg: message to be displayed
        """
        self.text_to_speech.display_msg(msg)
        self.gui.forward_to_frontend(msg, 'jade')

    def gui_display_sent_message(self, msg):
        """
        Should display message on GUI when received from speech-to-text.

        :param msg: message to be displayed
        """
        self.gui.forward_to_frontend(msg, 'user')

    def app_request(self, app, req):
        """
        Receives request for info from JadeApp and returns answer to request

        # TO-DO:
            - define standard for request responses

        :param app: string representation of JadeApp used
        :param req: string representation of request sent from app

        :return: answer to req from Hub
        """
        pass

    def initialize_app(self, app_name):
        """
        Initializes app in system. Following return of this function, all communications with the app should be enabled.

        # TO-DO: add error handling with try/catch exceptions. probably need to coordinate with class initializations?

        :param app_name: string representation of app to be initialized
        :return: 0 on success, 1 on failure
        """
        if app_name not in self.apps:
            print(app_name, "not in listed apps")
            return 1
        if self.apps[app_name][1]:
            print(app_name, "already initialized")
            return 1

        self.apps[app_name][1] = self.apps[app_name][0](app_name, self)
        self.apps[app_name][1].start()

        return 0

    def retrieve_func_tools(self, app):
        return self.apps[app][1].retrieve_func_tools()

    def handle_stt_state(self, stt_enabled):
        print("stt_enabled:", stt_enabled)
        self.speech_to_text.setEnabled(stt_enabled)

    def disable_stt(self):
        self.gui.disable_stt()
