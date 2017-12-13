#!/usr/bin/env python2
import requests
from utils import *
import json
import hashlib

def send_message(message,username,config):
    gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(username).hexdigest() + "?d=robohash&s=96"
    send_data = {
        "to":config["to_irc"],
	    "token":config["token"],
	    "text":message,
	    "sendAs":{
	    	"name":username,
	    	# "profileImage":"https://identicon-api.herokuapp.com/"+ username +"/96?format=png"
            "profileImage":gravatar_url,
	    },
	    "onBehalfOf":config["user"]
    }
    try:
        uid = requests.post(config["flock_url"],data=json.dumps(send_data))
        print_log(uid.text)
    except Exception as e:
        print(e)