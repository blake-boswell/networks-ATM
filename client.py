'''
ATM TCP Client
Author: Blake Boswell (modified DRT's TCPClient EX)
UAID: 010728180
usage: python3 client.py serverName serverPort
Checks the balance of an account, makes withdrawals, and makes deposits
'''

import sys
from socket import *

if sys.argv.__len__() != 3:
    serverName = 'localhost'
    serverPort = 8000
else:
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])



loggedIn = True
# print('Welcome to the ATM!\nType "logout" to logout')

# Get input from user

while loggedIn:
    # Create TCP connection
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # Connect to server
    clientSocket.connect((serverName, serverPort))
    request = input('Input request: ')
    print(request)
    if request == 'logout':
        loggedIn = False
    else:
        # Send it into socket to server
        requestBytes = request.encode('utf-8')
        clientSocket.send(requestBytes)

        # Receive response from server via socket
        response = clientSocket.recv(1024)

        print('From Server: {0}'.format(response.decode('utf-8')))
        clientSocket.close()

print('Logging out. Have a great day!')