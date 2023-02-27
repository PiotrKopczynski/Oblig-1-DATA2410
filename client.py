from socket import *
import sys

serverIP = sys.argv[1]
serverPort = int(sys.argv[2])
filename = sys.argv[3]
#python3 client.py 192.168.56.1 12220 index.html
#C:\Users\Piotkop\Documents\DATA2410\Oblig-1

connection = socket(AF_INET, SOCK_STREAM)

try: 
    connection.connect((serverIP, serverPort))
except Exception as e:
    print(e)
    print("ConnectionError")
    sys.exit()
connection.send(("GET /" + filename + " HTTP/1.1\n\n").encode())

response = ""
while True:
    data = connection.recv(1024).decode()
    print(data)
    if not data:
        break
    response += data

connection.close()

responseList = response.split('\n\n')

print("status code: ", responseList[0])
print("server response: ", responseList[1:])