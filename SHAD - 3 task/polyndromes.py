# -*- coding: utf-8 -*-
import sys
import string


def transform_e(a):
    if a == 'ё':
        a = 'е'
    return a


def compare_russian_words(a, b):
    return transform_e(a) == transform_e(b)


def check_polyndrome(sentence):
    split_symbols = string.whitespace + string.punctuation
    listed_str = [c.lower() for c in sentence if c.isalpha() and c not in split_symbols]
    return all([compare_russian_words(a, b) for a, b in zip(listed_str, reversed(listed_str))])


for i in range(int(input())):
    sentence = str(sys.stdin.readline())
    if check_polyndrome(sentence):
        print('yes')
    else:
        print('no')
