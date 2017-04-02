import os
import sys

dir = sys.argv[1]
# dir = '/Developer/ml-mipt/ml-mipt-part1/2017/lectures'

dir_content = os.listdir(dir)
# print os.stat(path).st_size

results = []
for file in dir_content:
    path = os.path.join(dir, file)
    if os.path.isfile(path):
        results.append((path, os.stat(path).st_size))

print(results)