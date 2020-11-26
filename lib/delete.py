import json
import os

os.chdir(r'/home/niko/data/Ralf')


def delete_server(server_id: str):
    if os.path.isfile("Server/{}.json".format(server_id)):
        os.remove(server_id)


def delete_giveaway(server_id: str, message_id: str):
    with open("Server/{}.json".format(server_id), 'r') as fp:
        data = json.load(fp)
    if message_id in data:
        del data[message_id]
    with open("Server/{}.json".format(server_id), 'w') as fp:
        json.dump(data, fp, indent=4)
