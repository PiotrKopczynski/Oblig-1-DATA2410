#import socket module
from socket import *
import sys # In order to terminate the program

#Prepare a sever socket
serverSocket = socket(AF_INET, SOCK_STREAM) 
serverPort = 12220
serverName = gethostbyname(gethostname())
try: 
        serverSocket.bind((serverName,serverPort))
except: # Handle bind error exception
    print("Bind failed. Error: ")
    sys.exit()
    
serverSocket.listen(1)

while True:
    #Establish the connection
    print("The server is listening :D")
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        print("GET request: ", message)
        filename = message.split()[1]
        filename = filename[1:]
        f = open(filename)
        outputdata = f.read()

        #Send one HTTP header line into socket
        connectionSocket.send(("HTTP/1.1 200 OK\n\n").encode())

        #Send the content of the requested file to the client 
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode()) 
        connectionSocket.send("\n\n".encode())
        # Close the connection socket
        connectionSocket.close()
         
    except IOError:
        #Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\n\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        #Close client socket
        connectionSocket.close()     
serverSocket.close()
sys.exit() #Terminate the program after sending the corresponding data