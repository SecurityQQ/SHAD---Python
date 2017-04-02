output = dict()

for i in range(int(input())):
    s = str(input()).lower()
    key_str = ''.join(sorted(list(s)))
    if key_str in output.keys():
        output[key_str].append(s)
    else:
        output[key_str] = [s]

for l in output.values():
    l.sort()

for strings in sorted(output.values()):
    unique_strings = sorted(list(set(strings)))
    if len(unique_strings) <= 1:
        continue
    for s in unique_strings:
        print(s, end=' ')
    print()
