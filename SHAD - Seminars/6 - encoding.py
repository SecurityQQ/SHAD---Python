# -*- coding: utf-8 -*-
import re
text = """In September 1769 she reached New
Zealand, the first European vessel to visit
in 127 years."""


def search_results(pattern, text):
    for m in re.finditer(pattern, text):
        print "'{0}': {1}-{2}".format(m.group(), m.start(), m.end())

# search_results('i', text)
#
# search_results(r'\\', '\\')
#
# search_results('.*', '12345')
#
# search_results('[0-9]{3,4}', text)
#
# search_results('e.*e', text)  # \n мешаеn

# В регулярках \s -- пробельные символы, \S - не пробельный символ, \d, \D ...

search_results('\st.*', text)

m = re.search('(\w+)\s*([0-9]+)', text)
print m.group(0)
print m.group(1)
print m.group(2)