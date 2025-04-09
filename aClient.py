from socket import *
import os
import time
from tkinter import simpledialog

from threading import Thread, Lock

# 196.47.ssg
CLIENT_G = "Awe"
SERVER_G = "Wola"
DISCONNECT = "bye"

PING = "PING"
PONG = "PONG"

STILLIN = "YES"

deviceName = ""


port = 19000
responses = []
outList = []
index = -1
fileSize = 0
currentData = 0

# Lock for list access by threads
lock = Lock()


#Connect to udp server
def conTracker(ip,choice):

    #udp socket
    sock = socket(AF_INET,SOCK_DGRAM)

    serverIP = ip
    serverPort = 17000

   
    
    if (choice == "a"):
        # Sharing files
        becomeSeeder(sock,(serverIP,serverPort))
    elif (choice == "b"):
        # Requesting files
        getFile(sock,(serverIP,serverPort))
    

    sock.close()
    

def outFile():
    while not outList:
        time.sleep(1)
    return outList




def setIndex(ind):
    global index
    index = ind

def getFile(sock,adress):
    # Get files available for download from sever
    message = CLIENT_G+":get"

    sock.sendto(message.encode(),adress)

    # Wait for response
    data, server = sock.recvfrom(1024*4)
    response = data.decode()
    response.strip()
    
    if len(response)>3:
        response = response.split(":")
        files = response[0].split("&")
        hosts = response[1].split("=")

        num = 1

        print("\n===================================================")
        print("Here are files available for download (Choose number)")       
        for x in files:
            print(str(num)+":   "+x)
            num = num+1



        global outList
        outList=files
        
        print()
        while index == -1:
            time.sleep(1)
        numChoice = index

        fileWanted = files[numChoice-1]
        fileHosts = hosts[numChoice-1].split("&")

        print("The file: "+fileWanted+" is hosted by")
        print(" and ".join(fileHosts))
        
        


        #Connecting to seeder with file
        client(fileWanted,fileHosts)

        print("===============================================")
        print("Download finished\n")

        print("Choose option")
        
        return 0
        choice = input("a: Become seeder\n b: Close system\n")

        # Sharing files
        if choice == "a":
            becomeSeeder(sock,adress)
        
    else:
        print("===============================================")
        print("No files to download!!!")

        
        

        print("Choose option")
        choice = input("a: Become seeder\n b: Close system\n")

        # Sharing files
        if choice == "a":
            becomeSeeder(sock,adress)

def getFiles():
    dir = os.getcwd()
    
    files = []
    for x in os.listdir(dir):
        file = os.path.join(dir, x)
        if os.path.isfile(file):
            files.append(x)
    
    return files
    

def becomeSeeder(sock,adress):

    
    message = CLIENT_G+":seed^"+deviceName+":"

    # Get the current working directory
    dir = os.getcwd()

    files = []


    # Getting list of all files in folder
    for x in os.listdir(dir):
        file = os.path.join(dir, x)
        if os.path.isfile(file):
            files.append(x)

    files = " ".join(files)

    message = message+files
    
    

    sock.sendto(message.encode(),adress)

     # Wait for response
    data, server = sock.recvfrom(1024)
    response = data.decode()
    if response:
        print(response)

        
        # thread to handle pinging
        thread = Thread(target=ping)
        thread.start()


        #TCP server waiting for communication CODE here
        tcpServer()
        

# pingingfunctionality
def ping():
    while True:
        
        # Sock to communicate with tracker for pinging
        with socket(AF_INET, SOCK_DGRAM) as sock:
            sock.bind(("0.0.0.0",20000))
            # Wait for tracker to ping
            data, server = sock.recvfrom(1024)

            if data:
                message = data.decode()

                if message == PING:
                    sock.sendto(PONG.encode(),server)
                    time.sleep(5)
                    
# get size of requested file
def totSize():
    return fileSize

# size of bytes already read
def progress():
    return currentData
    
# Code for tcp file sharing
def tcpServer():
    serverPort = 19000

    with socket(AF_INET, SOCK_STREAM) as serverSock:
        serverSock.bind(("0.0.0.0", serverPort))
        serverSock.listen(1)
        print("Listening on port", serverPort)

        #Waiting for contact from leecher
        while True:
            conSock, address = serverSock.accept()
            print("Connection from:", address)

            try:
                message = conSock.recv(1024).decode()
                message_parts = message.split(":")

                if message_parts[0] == "size":
                    # returning size of requested file
                    response = str(os.path.getsize(message_parts[1]))
                    conSock.send(response.encode())
                elif message_parts[0] == "get":
                    # returning list of hosted file and file hosts
                    fileName = message_parts[1]
                    start = int(message_parts[2])
                    end = int(message_parts[3])

                    response = readFile(fileName, start, end)
                    conSock.send(response)
            except Exception as e:
                print("An error occured")
            finally:
                conSock.close()


# Reading byte range of a given file
def readFile(fileName, start, end):
    try:
        with open(fileName, "rb") as file:
            file.seek(start)
            return file.read(end - start + 1)
    except Exception as e:
        print("Could not read file:",fileName)
        return b""


# Connecting to tcp server to get file
def conServer(ip, port, message, index):
    try:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect((ip, port))
            sock.send(message.encode())
            response = b""

            # Recieving server response in chunks
            
            while True:
                chunk = sock.recv(1024)  # Receive 1KB at a time
                
                # locking variable accessed by multiple threads
                with lock:
                    global currentData
                    currentData= currentData+ 1024
                
                if not chunk:
                    break
                response += chunk

            # Getting size of file wanted
            if "size" in message:
                print("File size: " + response.decode() + " bytes")
                return response.decode()
            # locking list accessed by multiple threads   
            with lock:
                if index != -1:
                    responses[index] = response
    except Exception as e:
        print("Could not connect to server " +ip)



# Code for TCP client
def client(fileWanted,servers):
    
    threads = []

    size = conServer(servers[0], port, "size:"+fileWanted, -1)
    
    global fileSize 
    fileSize =  int(size)
    
    ranges = split_range(int(size), len(servers))

    # Creating a list for threads to write their bytes reacived from seeder
    for n in servers:
        responses.append(b"")

    for index, ip in enumerate(servers):
        
        message = "get:"+fileWanted+":"+str(ranges[index][0])+":"+str(ranges[index][1])

        # Reaqusting file chunks from different hosts of the file
        thread = Thread(target=conServer, args=(ip, port, message, index))
        thread.start()
        threads.append(thread)

    output = b""
    for thread in threads:
        thread.join()
        output += responses[threads.index(thread)] # Putting file chunks together

    #Writing recieved bytes to file
    with open("copy_"+fileWanted, "wb") as out:
        out.write(output)


# Generating range split between hosts of files
def split_range(n, num_ranges):
    rangeLength = n // num_ranges    
    ranges = []
    for i in range(num_ranges):
        start = i * rangeLength

        if i != num_ranges - 1:
            end = (i + 1) * rangeLength-1
        else: 
            end = n-1

        ranges.append((start, end))
    
    return ranges






def go(serverName,devName,choice):
    global deviceName
    deviceName = devName
    #serverName = str(input("Enter server IP:\n"))
    
    print("\nWhat do you want to do? (choose letter)")
    print("========================")

    print("a: Become Seeder")
    print("b : Get file")

    
    conTracker(serverName,choice)

