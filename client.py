from socket import *
import sys

#Get inputs from command line
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])
filename = sys.argv[3]

connection = socket(AF_INET, SOCK_STREAM)

try: 
    connection.connect((serverIP, serverPort))
except:
    print("ConnectionError")
    sys.exit()
connection.send(("GET /" + filename + " HTTP/1.1\n\n").encode()) # Send HTTP GET request

response = "" # Variable for storing the server response
while True:
    data = connection.recv(1024).decode()
    print(data)
    if not data: # Break the loop if the response has ended
        break
    response += data

connection.close() #close the socket

responseList = response.split('\n\n')

# Print status code and the full server response
print("status code: ", responseList[0])
print("server response: ", responseList[1:])