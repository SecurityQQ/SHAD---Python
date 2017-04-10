graph = [
    [0, 1, 0, 1, 0, 0],
    [1, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0]
]


visited = [0] * len(graph)

next_v = [0]
visited[0] = 1
while len(next_v) > 0:
    cur_v = next_v[-1]
    next_v.pop()
    print("current_v: ", cur_v)
    for v in range(len(graph[cur_v])):
        if visited[v] == 0 and graph[cur_v][v] != 0:
            print(v)
            visited[v] = 1
            next_v.append(v)

