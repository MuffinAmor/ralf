import json
import os

from lib.create import create_server

os.chdir(r'/home/niko/data/Ralf')


def request_item(server_id: str, item: str, message_id: str):
    create_server(server_id)
    with open("Server/{}.json".format(server_id), 'r') as fp:
        data = json.load(fp)
    if message_id in data:
        return data[message_id][item]


def request_if(server_id: str, message_id: str):
    create_server(server_id)
    with open("Server/{}.json".format(server_id), 'r') as fp:
        data = json.load(fp)
    if message_id in data:
        return True
    else:
        return True


def request_giveaways(server_id: str):
    create_server(server_id)
    with open("Server/{}.json".format(server_id), 'r') as fp:
        data = json.load(fp)
    all_giva = []
    for i in data:
        all_giva.append(i)
    return all_giva
