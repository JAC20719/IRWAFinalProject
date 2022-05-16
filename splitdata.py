import sys
import random

file = sys.argv[1]
with open(file) as f:
    lines = f.readlines()
    random.shuffle(lines)
    lines = [l.strip() for l in lines]
    split = int(len(lines) * 0.7)
with open(file[:-4] + '-train.txt', 'w') as f:
    for line in lines[:split]:
        print(line, file=f)
with open(file[:-4] + '-dev.txt', 'w') as f:
    for line in lines[split:]:
        print(line, file=f)