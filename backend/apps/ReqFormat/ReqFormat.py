import types

from apps.ReqFormat.FuncWrap import FuncWrap
from apps.ReqFormat.ReqFormatException import ReqFormatException


class ReqFormat:
    def __init__(self, dictionary):
        if not isinstance(dictionary, dict):
            raise ReqFormatException("ReqFormat dictionary should be of type dict")

        # yeah maybe rename this later
        self.dictionary = dictionary

        for key, val in self.dictionary.items():
            if not isinstance(key, str):
                raise ReqFormatException("each key should be a string")
            if not isinstance(val, ReqFormat) and not isinstance(val, FuncWrap):
                raise ReqFormatException("val is not a ReqFormat or FuncWrap object")
