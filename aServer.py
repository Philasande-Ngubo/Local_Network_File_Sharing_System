from socket import *
import threading
CLIENT_G = "Awe"
SERVER_G = "Wola"
DISCONNECT = "bye"
PING = "PING"
PONG = "PONG"
STILLIN = "YES"

seeders = []
port = []
filesHosted = []
names = []

serverSock = None

        
        
    
def init():
    # Setting up udp socket
    global serverSock
    serverSock = socket(AF_INET,SOCK_DGRAM)
    serverAdress = ('0.0.0.0', 17000)
    serverSock.bind(serverAdress)

    # Setting up udp socket for pinging
    pingSock = socket(AF_INET,SOCK_DGRAM)
    pingAdress = ('0.0.0.0',21000)
    pingSock.bind(pingAdress)
    pingSock.settimeout(4)
    
    
    
    try:
        # Handle client messages
        while True:

            print("Server listening          PORT: "+ str(serverAdress[1]))
            print("======================================\n")
            # Receive data and client address
            data, clientAdress = serverSock.recvfrom(1024)
            
            message = data.decode()
            message = message.split(":")


            if message[0] == CLIENT_G:

                
                print("Connection request from",str(clientAdress[0]),"on Port: ",clientAdress[1])
                print("")

                # Request to become file host
                if "seed" in message[1]:
                    deviceName = message[1].split("^")[1]
                    addSeeder(clientAdress,deviceName,message[2])
                    response = "\nYou are now a seeder wait for leecher to make contact."
                    serverSock.sendto(response.encode(), clientAdress)

                # file request
                elif message[1] == "get":
                    ping(pingSock)
                    response = getFile()
                    serverSock.sendto(response.encode(), clientAdress)
                
    except KeyboardInterrupt:
        print("Shutting down server")

    finally:
        serverSock.close()
        
        
        
def ping(serverSocket):
    # pinging all seeders
    for x in seeders:
        dest = (x, 20000) #seeder adress
        try:
            serverSocket.sendto(PING.encode(),dest)
            
            data,clientAdress = serverSocket.recvfrom(1024)
            msg = data.decode()
            
            if msg == PONG:
                continue
        except timeout:
            # Remove seeder and its data if timeout occurs
            index = seeders.index(x)
            seeders.pop(index)
            port.pop(index)
            filesHosted.pop(index)
            names.pop(index)
   
def fileList():
    # Generating list of files in seeders
    files = []
    for x in filesHosted:
        x = x.split(" ")
        for file in x:
            
            if not file in files:
                files.append(file)

    return files

def getFile():

    # Generating list of all files being shared and corresponding hosts

    files = []
    hosts = []
    ipPos = 0
    pos = 0
    for x in filesHosted:
        x = x.split(" ")
        for file in x:
            
            if not file in files:
                files.append(file)
                pos = files.index(file)
                hosts.append(seeders[ipPos])
            else:
                pos = files.index(file)
                hosts[pos] = hosts[pos] +"&"+seeders[ipPos] 
            

        ipPos = ipPos+1
        
    a = "&".join(files) # files hosted 
    b = "=".join(hosts) # file hosts
    response = a+":"+b
    
    return response
        

# Adding new ip and files it has to list of file hosts
def addSeeder(ip,dName,dir):
    if (not ip[0] in seeders):
        seeders.append(ip[0])
        port.append(ip[1])
        names.append(dName)
        filesHosted.append(dir)

        print("New seeder IP:",ip[0], "\nSharing the following files:",dir)
        print()
    else:
        # Updating files share by host
        x = seeders.index(ip[0])
        filesHosted[x] = dir
        port[x] = ip[1]
        names[x] = dName
        print("seeder IP:",ip[0], "\nNow sharing the following files:",dir)
        print()

threading.Thread(target=init ).start()