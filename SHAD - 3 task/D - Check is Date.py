import re
import sys


date_regex = re.compile(r"""
                         (([0-9]{2})(?P<delim>[/.-])  # dd
                         ([0-9]{2})(?P=delim)  # mm
                         ([0-9]{4})$)|  # yyyy
                         (([0-9]{4})(?P<delim2>[/.-])    # yyyy
                         ([0-9]{2})(?P=delim2)  # mm
                         ([0-9]{2})$)|  # dd
                         ([0-9]{1,2})(\s*)  # d or dd
                         ([а-яА-ЯёЁ]+)(\s*)  # month
                         ([0-9]{4}$)  # year
                         """,
                        flags=re.UNICODE + re.VERBOSE)


def is_date(date):
    return re.match(date_regex, date) is not None

text = sys.stdin.readlines()
text[-1] += '\n'

for s in text:
    s = s[:-1]
    if is_date(s):
        print('YES')
    else:
        print('NO')
