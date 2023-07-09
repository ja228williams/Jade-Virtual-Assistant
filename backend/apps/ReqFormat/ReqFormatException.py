class ReqFormatException(Exception):
    def __init__(self, message):
        super().__init__("Request format malformed:", message)
