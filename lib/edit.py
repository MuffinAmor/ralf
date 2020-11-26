import json
import os

from lib.create import create_server

os.chdir(r'/home/niko/data/Ralf')


def edit_user(server_id: str, message_id: str, user_id: str, action: str):
    create_server(server_id)
    with open("Server/{}.json".format(server_id), 'r') as fp:
        data = json.load(fp)
    if action == "append":
        if user_id not in data[message_id]['user']:
            data[message_id]['user'].append(user_id)
            with open("Server/{}.json".format(server_id), 'w') as fp:
                json.dump(data, fp, indent=4)
    if action == "remove":
        if user_id in data[message_id]['user']:
            data[message_id]['user'].remove(user_id)
            with open("Server/{}.json".format(server_id), 'w') as fp:
                json.dump(data, fp, indent=4)


def edit_item(server_id, message_id: str, var: str, new):
    create_server(server_id)
    with open("Server/{}.json".format(server_id), 'r') as fp:
        data = json.load(fp)
    data[message_id][var] = new
    with open("Server/{}.json".format(server_id), 'w') as fp:
        json.dump(data, fp, indent=4)
