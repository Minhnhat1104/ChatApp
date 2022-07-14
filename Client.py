import socket
import os
import time
import threading

BUFFER_SIZE = 4096  # send 4096 bytes each time step
recieveInvitation = False
threads = list()


def init():
    # ------------Cac ham thuong xuyen dung------------

    def clearConsole():
        command = 'clear'
        if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
            command = 'cls'
        os.system(command)

    # ------------Client-sever section----------------

    def chooseSever():
        global SERVER_ADDRESS
        SERVER_ADDRESS = input("Pls choose Sever address: ")
        global PORT
        PORT = 12121

    def createClient():
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        try:
            soc.connect((SERVER_ADDRESS, PORT))
            print("Connected!")
            handleConnection(soc)
            soc.close()
        except:
            print("Server hasn't been install: ")
        finally:
            soc.close()

    def handleListen(soc, s1):
        msg = ["", ""]
        while msg[1] != "good-bye":
            msg = soc.recv(BUFFER_SIZE).decode("utf8").split('|')
            if msg[0] != str(soc.getsockname()):
                templateMsg = '{addr}: {msg}'
                print(templateMsg.format(addr=msg[0], msg=msg[1]))
            else:
                s1.release()

    def handleConnection(soc):
        s1 = threading.Semaphore(0)
        listenThread = threading.Thread(
            target=handleListen, args=(soc, s1), daemon=True)
        threads.append(listenThread)
        listenThread.start()
        msg = ""
        while msg != "quit":
            msg = input()
            soc.send(bytes(msg, "utf8"))
            s1.acquire()

    def start():
        clearConsole()
        chooseSever()
        createClient()

    start()


if __name__ == "__main__":
    init()
