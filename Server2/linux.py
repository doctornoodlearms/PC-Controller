from socketserver import *
from threading import *
import pyautogui
import screeninfo
import socket
import os

class UDPhandler(BaseRequestHandler):

    def __init__(self, request:tuple, client_address:tuple, server:UDPServer):


        self.request:tuple = request
        self.serverSocket:socket.socket = request[1]
        self.client_address:tuple = client_address
        self.server:UDPServer = server

        self.data: str = bytes(self.request[0]).strip().decode("utf-8")

        print(request)
        
        print("Request Recieved: {address}; {request}".format(address = client_address, request = self.data))

        global targetIP
        global targetHost
        
        self.handle()

    def handle(self):
        
        cmd = self.parseData(self.data)

        execute = cmdDict.get(cmd[0])
        if(execute != None):

            print("Executing Command:\n\tName: {name}\n\tArgs: {args}".format(name=cmd[0], args=cmd[1]))
            execute(cmd[1])
        
        else:

            print("Invalid Command: {name}".format(name=cmd[0]))
        
    
    # Command Structure
    # c={command}&arg1={value}
    def parseData(self, requestData:str):

        cmdName = ""
        cmdArgs = list()
        for i in requestData.split("&"):
            
            arg = i.split("=")
            if(len(arg) > 0):
                if(arg[0] == "c"):
                
                    cmdName = str(arg[1]).lower()
                else:
                    
                    cmdArgs.append(arg[1])

        return (cmdName, cmdArgs)

    def sendResponse(self, message):
        
        print("Sending response: " + message)
        self.serverSocket.sendto(message.encode(), self.client_address)

def _init():

    # Change This IP
    host:str = input("Current IP: ")
    port:int = 4242

    server = UDPServer((host, port), UDPhandler)
    print("Started Server")
    print(server.socket)
    server.serve_forever()

def com_OpenUrl(value):

    os.system("x-www-browser " + value)


    cmdDict = {

        "open":"com_OpenUrl"
    }