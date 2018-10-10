'''
ATM Server
Author: Blake Boswell (Modified from DRT's TCPServer EX)
UAID: 010727180
usage: python3 server.py serverPort
Maintains a bank account for a single user to access with (to avoid synchronization problems)
- Maintain the balance, do withdrawals, deposits, and respond to queries on the account balance
- User will talk to the server via client to check the balance, withdraw money, deposit money
- Server init bank balance to $10,000
'''


import sys
from socket import *

BUFFER_SIZE = 1024

class Account:
    
    def __init__(self):
        self.balance = 10000

    def getBalance(self):
        return self.balance

    def setBalance(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        if amount <= self.balance and amount >= 0:
            self.balance -= amount
            return True
        else:
            return False

    def deposit(self, amount):
        if amount >= 0:
            self.balance += amount

    def balanceAction(self):
        response = 'Balance: ${}'.format(self.balance)
        return response

    def withdrawAction(self, amount):
        didWithdraw = self.withdraw(amount)
        if didWithdraw:
            response = 'Successfully withdrew ${}.\nRemaining balance: ${}'.format(amount, self.balance)
        else:
            response = 'Failed to withdraw amount: ${}\nCurrent balance: ${}'.format(amount, self.balance)
        return response

    def depositAction(self, amount):
        if amount >= 0:
            self.deposit(amount)
            response = 'Added ${} to your account.\nNew balance: ${}'.format(amount, self.balance)
        else:
            response = 'Failed to deposit. Nice try, you cannot deposit that which doesn\'t exist.'
        return response

# Set port
if sys.argv.__len__() != 2:
    # Only one argument after the filename, port is missing
    serverPort = 8000
else:
    serverPort = sys.argv[2]

# Listen on welcome socket
serverSocket = socket(AF_INET, SOCK_STREAM)
# The SO_REUSEADDR flag tells the kernel to reuse a local socket
# in TIME_WAIT state, without waiting for its natural timeout to expire.
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))
# If there is more than one unaccepted connection, the sys will refuse new connections
serverSocket.listen(1)
print('Listening on port {}'.format(serverPort))

# Only handling one user, so the program gets one shared account
user = Account()


# Loop, listening for requests on the welcome socket
while 1:
    # When a request comes in, create a connection socket to handle request
    # Address is the connectionSocket's address
    (connectionSocket, address) = serverSocket.accept()
    # Recieve request bytes
    request = connectionSocket.recv(BUFFER_SIZE)
    # Decode bytes to utf-8
    requestString = request.decode('utf-8')

    # Split the request to extract command, and the optional amount
    requestArguments = requestString.split(' ')
    numArguments = len(requestArguments)

    if numArguments > 1:
        amount = int(requestArguments[1])
    action = requestArguments[0]

    if action == 'balance':
        responseString = user.balanceAction()
    elif action == 'withdraw':
        responseString = user.withdrawAction(amount)
    elif action == 'deposit':
        responseString = user.depositAction(amount)
    elif action == 'logout':
        responseString = False
    else:
        responseString = 'Unknown command. Please use one of the following\n\tbalance: Checks the balance in the account\n\twithdraw [amount]: Withdraw $[amount] from the account\n\tdeposit [amount]: Deposits $[amount] into the account\n\tlogout: End the connection'

    if responseString:
        response = responseString.encode('utf-8')
        # Respond to user
        connectionSocket.send(response)
    # Close connection
    connectionSocket.close()