import sys
from functools import wraps
from copy import deepcopy


class Self_Generator(object):
    def __init__(self, generator, args, kwargs):
        self.generator = generator
        self.args = deepcopy(args)
        self.kwargs = deepcopy(kwargs)

    def __iter__(self):
        return self.generator(*self.args, **self.kwargs)

    def __next__(self):
        return next(iter(self))


def inexhaustible(g_func):
    @wraps(g_func)
    def wrapped_func(*args, **kwargs):
        return Self_Generator(g_func, args, kwargs)

    return wrapped_func


exec(sys.stdin.read())
