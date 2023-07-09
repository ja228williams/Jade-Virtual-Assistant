import types

from apps.ReqFormat.ReqFormatException import ReqFormatException


class FuncWrap:
    def __init__(self, func, args):
        if not isinstance(func, types.FunctionType):
            raise ReqFormatException('func should be of type function')
        self.func = func

        if args is not None and not isinstance(args, list):
            raise ReqFormatException('args should be a list')
        for arg in args:
            if not isinstance(arg, str):
                raise ReqFormatException('each argument should be a string')
        self.args = args if args else []

    def apply(self):
        return lambda: self.func(self.args)
