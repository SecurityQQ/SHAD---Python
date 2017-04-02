import sys
from collections import Counter

dictionary = dict()
read_dictionary = True


for s in iter(sys.stdin):
    s = s[:-1]
    if len(s) == 0:
        read_dictionary = False
        continue

    if read_dictionary:
        lang, alphabet = s.split()
        # print(lang, alphabet)
        for c in alphabet:
            dictionary[c] = lang
        continue

    # print(dictionary)

    ans = []
    for word in s.split(' '):
        word = word.lower()
        # print('WORD: ', word)
        counted_languages = Counter([dictionary[c] for c in word if c in dictionary])
        # print(counted_languages)
        if len(counted_languages) == 0:
            continue
        ans.append(sorted([l for l, num in counted_languages.items()
                           if num == counted_languages.most_common(1)[0][1]])[0])

    # print (ans)

    print(' '.join(sorted(list(set(ans)))))
