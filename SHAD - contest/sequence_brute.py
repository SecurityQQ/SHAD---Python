import sys


n = int(sys.stdin.readline())
a = list(map(int, sys.stdin.readline().split()))

maximum = a[0]

for d in range(1, n):
    for start in range(0, n - d):
        for end in range(start + d, n + 1):
            now_sum = sum(a[start:end:d])
            maximum = max(maximum, now_sum)

print(maximum)