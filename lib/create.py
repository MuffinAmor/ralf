import json
import os

os.chdir(r'/home/niko/data/Ralf')


def create_server(server_id: str):
    if not os.path.isdir("Server"):
        os.mkdir("Server")
    if not os.path.isfile("Server/{}.json".format(server_id)):
        data = {}
        with open("Server/{}.json".format(server_id), 'w') as fp:
            json.dump(data, fp, indent=4)


def create_giveaway(server_id: str, channel_id: str, message_id: str, hoster_id: str, start_var, time_var, winner: int):
    create_server(server_id)
    with open("Server/{}.json".format(server_id), 'r') as fp:
        data = json.load(fp)
    data[message_id] = {
        'channel': channel_id,
        'user': [],
        'activ': True,
        'hoster': hoster_id,
        'start': start_var,
        'time': time_var,
        'winner': winner

    }
    with open("Server/{}.json".format(server_id), 'w') as fp:
        json.dump(data, fp, indent=4)
