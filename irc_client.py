#!/usr/bin/env python2
import socket
import datetime
import json
import time
from utils import print_sending_log, print_log

class IRC:
    __ping__ = 'PING'
    __pong__ = 'PONG'
    server=''
    port=0
    nick="flockbot"
    name = "Flock Bot"
    pwd = ""
    sock=None
    channels=[]
    callback=None
    motd=False
    pwdSet=False

    def __init__(self, server, port, **kwargs):
        self.server=server
        self.port = port
        if len(kwargs)>0:
            if 'nick' in kwargs:
                self.nick = kwargs['nick']
            if 'pwd' in kwargs:
                self.pwd = kwargs['pwd']
    def __send_message__(self, command, message):
        self.sock.send(command+" "+message+"\r\n")
        print_sending_log(command+" "+message)

    def __parse_message__(self, message):
        prefix='' 
        command=''
        arg=''
        if message[0] == ':':
            prefix, message = message[1:].split(' ',1)
        if message.find(' :') != -1:
            message, trailing = message.split(' :', 1)
            args = message.split()
            args.append(trailing)
        else:
            args = message.split()
        command = args.pop(0) 
        self.__handle_message__(prefix, command, args)

    def __handle_message__(self, prefix, command, args):
        # Handle PING
        if prefix=="" and command.startswith(self.__ping__):
            self.__send_message__(self.__pong__, args[0])
        
        # Cases for messages
        if 'PRIVMSG' in command:
            user = ''
            if '!' in prefix:
                parts = prefix.split('!')
                user = parts[0]
                ip = parts[1].replace("~",'').split('@')[1]
                self.__dump_message__({
                    'ip':ip,
                    'from':user,
                    'to':args[0],
                    'message':args[1].replace("\r\n",''),
                    'command':command,
                    'timestamp':time.time()
                    })

    def __establish_socket__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10)
        self.sock.connect((self.server, self.port))
        self.sock.settimeout(None)
        self.__send_message__('NICK',self.nick)
        self.__send_message__('USER', self.nick +' '+self.name+" "+self.nick)
    
    def __start_socket_listener__(self):
        while True:
            data = self.sock.recv(2048)
            if len(data) > 0:
                if not self.motd:
                    if "This nickname is registered." in data:
                        self.motd=True
                        if self.pwd!="":
                            self.__send_message__("PRIVMSG","NICKSERV :identify "+self.pwd)
                elif not self.pwdSet and self.pwd!="":
                    if "NOTICE" in data and "You are now identified for" in data:
                        self.pwdSet=True
                        self.__join_channels__()
                elif self.pwd=="":
                    self.__join_channels__()
                self.__parse_message__(data)

    def __join_channels__(self):
        for channel in self.channels:
            print_log("Joining channel: "+ channel)
            self.__send_message__("JOIN", channel)
    
    def __dump_message__(self,  message):
        if self.callback != None:
            self.callback(message)

    def set_pwd(self, pwd):
        self.pwd = pwd

    def dump_callback(self, callback):
        self.callback = callback

    def send_message(self, to, message):
        message=to+":"+message
        __send_data_on_socket__(message)

    def join_channel(self, channel):
        if channel not in self.channels:
            self.channels.append(channel)

    def start_client(self):
        self.__establish_socket__()
        self.__start_socket_listener__()