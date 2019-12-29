import os
dir = ""
path = os.getcwd()
print(path)
if '/' in path:
    path = path.split('/')
    path.pop()
    for p in path:
        dir = dir + p + '/'
if '\\' in path:
    path = path.split('\\')
    path.pop()
    for p in path:
        dir = dir + p + '\\'
print(dir)
