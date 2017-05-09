import sys
from collections import Counter
from bisect import bisect_left

n = int(sys.stdin.readline())
a = list(map(int, sys.stdin.readline().split()))

counted = Counter(a)

def split_less(a, ind):
    left = [i for i in range(0, ind) if a[i] < a[ind]]
    right = [i for i in range(ind + 1, len(a)) if a[i] < a[ind]]
    return left + right

def get_tree(a):
    tr = [split_less(a, i) for i in range(len(a))]
    return tr

def dfs(tree, i, current_height, l, r):
    # print(tree, i, current_height, l, r)
    ans = current_height

    l_bound = bisect_left(tree[i], l)
    r_bound = bisect_left(tree[i], r)
    for ix in tree[i][l_bound:r_bound]:
        if ix > i:
            ans = max(ans, dfs(tree, ix, current_height + 1, i, r))
        else:
            ans = max(ans, dfs(tree, ix, current_height + 1, l, i))
    # print(ans)
    return ans


tree = get_tree(a)
print(max([dfs(tree, i, 0, l=0, r=n-1) for i in range(n)]) + 1)
