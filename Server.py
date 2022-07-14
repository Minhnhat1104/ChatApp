import socket
import os
import threading

numberOfclient = 20
BUFFER_SIZE = 4096  # send 4096 bytes each time step
threads = list()
clientConnections = []


def init():
    # ------------Cac ham thuong xuyen dung------------

    def clearConsole():
        command = 'clear'
        if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
            command = 'cls'
        os.system(command)

    # ------------Client-sever section----------------

    def getInfo():
        global HOST_NAME
        HOST_NAME = socket.gethostname()
        global HOST_ADDRESS
        HOST_ADDRESS = socket.gethostbyname(HOST_NAME)
        print(HOST_NAME)
        print(HOST_ADDRESS)

    def choosePort():
        global PORT
        PORT = 12121

    def createServer():
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.bind((HOST_ADDRESS, PORT))  # tuple
        soc.listen(2)
        nClient = 0
        try:
            while nClient < numberOfclient:
                try:
                    clientConnection, clientAddr = soc.accept()
                    clientConnections.append(clientConnection)
                    nClient += 1
                    print("Connected to Client: ", clientAddr)
                    x = threading.Thread(
                        target=handleConnection, args=(clientConnection, clientAddr), daemon=True)
                    threads.append([x])
                    x.start()
                    nClient -= 1
                except:
                    print("Client's connection error")
        finally:
            soc.close()

    def handleConnection(clientConnection, clientAddr):
        msg = ""
        while msg != "quit":
            msg = clientConnection.recv(1024).decode("utf8")
            tempplateMsg = '{clientAddr}: {msg}'
            print(tempplateMsg.format(clientAddr=clientAddr, msg=msg))
            for i in range(len(clientConnections)):
                clientConnections[i].send(
                    bytes('|'.join([str(clientAddr), msg]), 'utf8'))

    def start():
        clearConsole()
        getInfo()
        choosePort()
        createServer()

    start()


if (__name__ == "__main__"):
    init()
