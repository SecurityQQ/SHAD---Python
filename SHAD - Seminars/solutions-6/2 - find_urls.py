# -*- encoding: utf-8 -*-


"""Finding urls in text."""


import re


URLS_PATTERN = re.compile(
    r'(https?://|www\.)((\w|-)+\.)+\w+(:[0-9]+)?(/(\w|-|\.)+)*/?')


def find_urls(text):
    """Generate a list of all urls in the text."""
    for match in URLS_PATTERN.finditer(text):
        yield match.group(0)
