import requests
from flask import Flask, request, jsonify
import json

PORT_FRONTEND = 3001
PORT_BACKEND = 3002

app = None


class GUI:
    def __init__(self, hub):
        print('initializing gui...')
        self.hub = hub

        self.app = Flask(__name__)
        self.register_routes()

    def start(self):
        return self.run_app()

    def run_app(self):
        # signal to user that backend is setup
        self.forward_to_frontend("How can I help you?", "jade")
        
        self.app.run(host='127.0.0.1', port=PORT_BACKEND)
        print("monitoring port", PORT_BACKEND)

    # @app.endpoint()
    def register_routes(self):
        @self.app.route("/", methods=["POST"])
        def handle_post_request():
            print('received request!')
            print('request:', request)

            data = request.get_json()
            print("data:", data)
            print("completed")

            if 'msg' in data:
                self.hub.receive_msg(data['msg'])
            elif 'stt_enabled' in data:
                self.hub.handle_stt_state(data['stt_enabled'])
            else:
                raise Exception('Request malformed: ' + str(data))
            return data

    def frontend_post(self, data):
        url = 'http://localhost:' + str(PORT_FRONTEND)
        print('forwarding to front-end:', data)
        response = requests.post(url, json.dumps(data))
        return 1 if response.status_code == 200 else 0

    def forward_to_frontend(self, msg, sender):
        data = {
            "msg": msg,
            "sender": sender
        }
        return self.frontend_post(data)

    def disable_stt(self):
        data = {
            "stt": "disabled"
        }
        return self.frontend_post(data)
