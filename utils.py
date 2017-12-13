import datetime

def print_sending_log(message):
    print(datetime.datetime.now().strftime('%H:%M:%S')+" SENDING :: "+message)

def print_log(message):
    print(datetime.datetime.now().strftime('%H:%M:%S')+" "+message)