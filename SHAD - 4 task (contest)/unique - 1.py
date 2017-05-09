import sys


def unique(iterable):
    last = None
    for it in iterable:
        if it != last:
            yield it
        last = it


exec(sys.stdin.read())
