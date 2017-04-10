import re
import sys
from collections import Counter

from_import_regex = re.compile(r'from +([^\s;]+)\s+import\s+([^;\n]+)[;\n]')
imports_all = re.compile(r'import\s+([^;\n]+)[;\n]')

text = ''.join(sys.stdin.readlines())+'\n'
# text = """import sys
# import math
# from os import path
#
# def f(a):
#     if a == 0:
#         import re"""


from_modules = [s[0] for s in re.findall(from_import_regex, text)]
from_imports_not_splited = [s[1] for s in re.findall(from_import_regex, text)]
all_imports_not_splited = re.findall(imports_all, text)


def ll_to_l(ll):  # merges list of lists of strings into list
    ans = []
    for l in ll:
        ans += l
    return ans


def unique(l):
    return list(set(l))


def split_modules(l):
    no_spaces = ll_to_l([s.split() for s in l])
    no_commas = ll_to_l([s.split(',') for s in no_spaces])
    return unique([s for s in no_commas if len(s) > 0])


from_imports = Counter(split_modules(from_imports_not_splited))
all_imports = split_modules(all_imports_not_splited)
imports_not_with_from = Counter(all_imports) - from_imports

# print(from_imports)
# print(all_imports)
# print(imports_not_with_from)

ans = sorted(from_modules + [s for s in imports_not_with_from.keys()])
print(', '.join(ans))
