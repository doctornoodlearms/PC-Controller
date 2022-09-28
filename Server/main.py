from socketserver import *
from threading import *
import win32, win32api, win32con
import screeninfo
import socket

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
        
        if(self.data == "connect"):

            if(targetIP == ""):

                # resolvedHost = socket.gethostbyaddr(self.client_address[0])[0]
                # print(resolvedHost)

                # if(targetHost == resolvedHost):

                #     print("Updated Client: "+targetHost)
                #     targetIP = self.client_address[0]
                self.sendResponse("connected")
                return

            elif(targetIP == client_address[0]):
                print("Client Reconnecting")
                self.sendResponse("connected")
                return

        # if(targetIP != client_address[0]):
        #     return
        
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

    host:str = "10.1.92.253"
    port:int = 4242

    server = UDPServer((host, port), UDPhandler)
    print("Started Server")
    print(server.socket)
    server.serve_forever()


def com_MoveMouse(args=[0,0]):
    
    currentPos = win32api.GetCursorPos()
    newPos = (round(float(args[0]) + currentPos[0]), round(float(args[1]) + currentPos[1]))
    win32api.SetCursorPos(newPos)

def com_MouseLeftClick(args=[]):

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def com_MouseLeftDown(args=[]):

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)

def com_MouseLeftUp(args=[]):

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def com_MouseRightClick(args=[]):

    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

def com_PanVerticle(args=[]):

    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, round(float(args[0])))

def com_PanHorizontal(args=[]):

    win32api.mouse_event(win32con.MOUSEEVENTF_HWHEEL, 0, 0, round(float(args[0])))

def getResolution():

    for i in screeninfo.get_monitors():

        if(i.is_primary == True):
            
            return (i.width, i.height)

targetHost = "Galaxy-J7-Crown"
targetIP = ""
cmdDict={

    "leftmouseclick" : com_MouseLeftClick,
    "leftmousedown" : com_MouseLeftDown,
    "leftmouseup" : com_MouseLeftUp,
    "movemouse" : com_MoveMouse,
    "rightmouseclick" : com_MouseRightClick,
    "panverticle" : com_PanVerticle,
    "panhorizontal" : com_PanHorizontal
}
_init()