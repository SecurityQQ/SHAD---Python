import sys


class AssertRaises(object):
    def __init__(self, exception):
        self.exception = exception

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        print(type, value, traceback)
        if issubclass(type, self.exception)  value is None:
            return True
        else:
            raise AssertionError

# exec(sys.stdin.read())
try:
    with AssertRaises(TypeError):
        pass
except Exception as e:
    print(type(e).__name__)