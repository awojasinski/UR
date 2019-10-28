import json

with open('config.json', 'r') as config_file:
    data = config_file.read()

config = json.loads(data)
print("host: " + str(config['connection']['host']))
print("port: " + str(config['connection']['port']))
print("------------------------------")
print("computer vision mode: " + str(config['cvision']['type']))
print("------------------------------")
j = 1
for i in config['cvision']['order']:
    print(str(j) + ". " + str(i))
    j = j+1