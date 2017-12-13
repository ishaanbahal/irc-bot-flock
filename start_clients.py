#!/usr/bin/env python2
import json
import flock
import irc_client
from utils import *

class ClientHandler:
    config={}
    
    def __init__(self, config):
        self.config=config
    
    def irc_callback_flock_message(self, message):
        channel = message["to"]
        if channel in self.config:
            flock.send_message(message["message"],message["from"],self.config[channel])
        else:
            print_log("Channel not in config, please update config for channel: "+channel)


def parse_config(path):
    config = json.loads(open(path).read())
    return config

def main():
    config = parse_config("config.json")
    client = ClientHandler(config["channels"])
    irc = irc_client.IRC("chat.freenode.net",6667, pwd=config["auth"]["pwd"], nick=config["auth"]["nick"])
    for channel in config["channels"]:
        irc.join_channel(channel)
    irc.dump_callback(client.irc_callback_flock_message)
    irc.start_client()

if __name__=="__main__":
    main()