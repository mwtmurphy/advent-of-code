'''error module'''

class Error(Exception):
    '''default exception handler'''
    def __init__(self, msg):
        self.msg = msg

class ArgError(Error):
    '''handle for function argument type errors'''

class EnvError(Error):
    '''handle for environment variable errors'''
    pass

class FormatError(Error):
    '''handle for argument format errors'''
    pass