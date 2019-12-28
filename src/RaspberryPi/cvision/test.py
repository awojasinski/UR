import os

path = os.getcwd()
path = path.split('/')
path.pop()
dir = ""
for p in path:
    dir = dir + p + '/'
print(dir)
