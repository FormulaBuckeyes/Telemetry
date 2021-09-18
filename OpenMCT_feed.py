# Data provider for the Aircraft_42 implementation
# Grabs Data from Mission Planner
# sends data to a specified UDP port
# Threading implemented to support the sending of commands without blocking the data forwarding to the OpenMCT Telemetry Server
# in this stage not inteded to be used on a real aircraft, only simulation. Threading and usage of sockets need to be improved

import socket
import time
from threading import Thread, Lock
import sys

UDP_IP = "127.0.0.1" #standard ip udp (localhost)

keys = {}
mutex = Lock()

def sendToMCT(run):

    UDP_PORT_SEND = 50015   #chosen port to OpenMCT (same as in telemetry server object)
    MESSAGE = "" #init message

    # initiate socket and send first message
    sockSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP

    while True:
        mutex.acquire()
        try:
            for key, value in keys.items():
                if (value):
                    timeStamp = time.time()
                    MESSAGE = "{},{},{}".format(key,100,timeStamp)
                    sockSend.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT_SEND))
                    time.sleep(0.1)
        finally:
            mutex.release()

        if not(run()): #to kill the thread
            print('Message Pump Closed!')
            break
 

def command(run):

    UDP_PORT_RCV = 50016   #chosen port to OpenMCT (same as in telemetry server object)
    data = ''
    addr = ''
    connected = False

    # initiate socket and send first message
    sockRcv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
    try:
        sockRcv.bind((UDP_IP, UDP_PORT_RCV)) # bind the socket to the specified ip and port
        sockRcv.setblocking(0) # set the socket on unblocking, so we wont get stuck on sockRcv.recvfrom()
        connected = True # if connected go into the loop
    except:
        print('Connecting to Telemetry Server failed! Wait a couple of seconds, so the socket will close. Then restart the script.')
        sockRcv.close() # if connection fails retry
        

    while connected:
        try:
            data, address = sockRcv.recvfrom(1024) # buffer size is 1024 bytes
            parts = data.decode("utf-8").split(" ")
            options.get(parts[0], lambda: "Unknown command")(parts[1])
        except socket.error:
            pass
    
    
        if not(run()): #to kill the thread
            sockRcv.close()
            print('Command Closed!')
            break

def subscribe(id):
    mutex.acquire()
    keys[id] = True
    print("subscribed " + id)
    mutex.release()

def unsubscribe(id):
    mutex.acquire()
    keys[id] = False
    print("unsubscribed " + id)
    mutex.release()

options = {
    "subscribe": subscribe,
    "unsubscribe": unsubscribe
}



    
#set the run argument true
run = True

# start the threads
sendMsgfromMP = Thread(target=sendToMCT,args=(lambda : run, ))
sendMsgfromMP.start()

command = Thread(target=command,args=(lambda : run, ))
command.start()



while True:
    try: #keep the main thread alive
        time.sleep(1)
    except: # on closing the main thread also close the function threads
        run=False 
        sendMsgfromMP.join()
        command.join()
        print('Ended!')
        sys.exit()

        



