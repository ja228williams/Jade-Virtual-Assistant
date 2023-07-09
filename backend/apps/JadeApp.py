# superclass for all jade apps

class JadeApp:
    def __init__(self, name, hub):
        print("starting JadeApp " + name + "...")
        # override this in subclass
        # req_format is a dictionary mapping string keys to either sub-req_formats representing subchoices or to
        # functions
        self.func_tools = None

        self.name = name
        self.hub = hub

    def start(self):
        # for now, all processing handled in subclasses
        return

    def app_request(self, req):
        # send request to hub
        self.hub.app_request(req)

    def hub_request(self, req):
        # should be received from hubappadpt- handle here. pretty much all functionality builds on this
        print(self.name, "received request...")

    def retrieve_func_tools(self):
        return self.func_tools

