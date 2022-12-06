import socket
import threading
import random
from datetime import datetime
import pytz

PORT = 55555
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind((SERVER, random.randint(8000, 9000)))

#COMMAND LIST
JOIN_COMMAND = "/join"
LEAVE_COMMAND = "/leave"
REGISTER_COMMAND = "/register"
ALL_COMMAND = "/all"
MSG_COMMAND = "/msg"
HELP_COMMAND = "/?"

#Receives stuff from server
def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except:
            pass

t = threading.Thread(target=receive)
t.start()

#Sends stuff to server. We code here.
def command_to_json(command, argument, name):
    if command.startswith(LEAVE_COMMAND):
        str = '{ "command": "/leave" , "owner": "'+ name +'"}'
        return bytes(str, 'utf-8')
        
    elif command.startswith(JOIN_COMMAND): 
        str = '{ "command": "/join", "owner": "'+ name +'" }'
        return bytes(str, 'utf-8')

    elif command.startswith(REGISTER_COMMAND):
        alias = argument                                                                    
        str = '{ "command": "/register", "owner": "'+ name +'", " "alias": "'+ alias +'" }'
        return bytes(str, 'utf-8')

    elif command.startswith(ALL_COMMAND):
        msg_to_client = argument
        message = '{ "command": "/all", "owner": "'+ name +'", "message": "' + msg_to_client + '" }'
        return bytes(message, 'utf-8')

    elif command.startswith(MSG_COMMAND):
        argument = argument.split(" ", 1)
        message = '{ "command": "/msg", "owner": "'+ name +'", "message": "' + argument[1] + '", "receiver: "' +  argument[0] + '" }'
        return bytes(message, 'utf-8')
    
    else:
        return b'{ "command": "" }'


name = "user_" + datetime.now(pytz.timezone('Singapore')).strftime("%d%m%Y%H%M%S") #temporary username/alias
print(f"\"{name}\" has been set as your temporary name. Use the /register command to register a new name.")
while True:
    message = input(f"/{name}:~>> ")

    input_tokens = message.split(" ", 1)
    command = input_tokens[0]

    argument = ""
    if len(input_tokens) > 1:
        argument = input_tokens[1]
    
    if message.startswith(HELP_COMMAND):
        print("\nThis is a list of commands\n/join - Join the chatroom\n/leave - Leave from the chatroom\n/register [alias] - Register to the chatroom\n/all [message] - Message all users\n/msg [alias] [message] - Message user with certain alias\n/? - Shows list of commands")

    elif message.startswith(JOIN_COMMAND) or message.startswith(ALL_COMMAND) or message.startswith(MSG_COMMAND) or message.startswith(REGISTER_COMMAND) or message.startswith(LEAVE_COMMAND):
        json_message = command_to_json(command, argument, name) 
        client.sendto(json_message, ADDR)
    
    else:
        print(f"{command} is not a recognized as a command by the program.\nPlease type \"/?\" for a list of commands.")  #Error message for unrecognized command