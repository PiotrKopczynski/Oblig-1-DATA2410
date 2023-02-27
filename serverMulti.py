from socket import *
import threading
import sys
import time

def now():
    """
    returns time of day
    """
    return time.ctime(time.time())


def handleClient(connectionSocket):
    """
    a client handler function
    """

    while True:
        try:
            message = connectionSocket.recv(1024).decode()
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
            break
         
        except IOError:
            #Send response message for file not found
            connectionSocket.send("HTTP/1.1 404 Not Found\n\n".encode())
            connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
            #Close client socket
            connectionSocket.close()
            break




def main():
    """
    creates a server socket, listens for new connections,
    and spawns a new thread whenever a new connection joins
    """
    serverSocket = socket(AF_INET, SOCK_STREAM) 
    serverPort = 12220
    serverName = gethostbyname(gethostname())

    try:
        serverSocket.bind((serverName,serverPort))
    except:
        print("Bind failed. Error: ")
        sys.exit()

    serverSocket.listen(1)

    while True:
        #Establish the connection
        print("The server is listening :D")
        connectionSocket, addr = serverSocket.accept()
        print("Server connected by ", addr)
        print(" at ", now())

        client_thread = threading.Thread(target=handleClient, args=(connectionSocket,))
        client_thread.start()

    serverSocket.close()

if __name__ == '__main__':
    main()
