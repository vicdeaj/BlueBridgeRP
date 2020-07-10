import threading
from time import sleep

import bluetooth


class StreamThread(threading.Thread):
    def __init__(self, serverSock, clientSock):
        super().__init__()
        self.othread = None
        self.serverSock = serverSock
        self.clientSock = clientSock
        self.cont = True

    def setup(self, othread):
        self.othread = othread

    def stop(self):
        self.cont = False
        self.clientSock.close()
        print("Thread stopped", self.name)


    def run(self):
        while self.cont:
            try:
                i = self.serverSock.recv(1024)

                #print("received: ", i)
            except ConnectionResetError:
                print("connection reset by peer")
                break
            except BlockingIOError:
                continue
            except bluetooth.BluetoothError as e:
                if "Resource temporarily unavailable" in str(e):
                    continue
                if "Connection reset by peer" in str(e):
                    print("BT connection reset by peer")
                    break
                else:
                    raise bluetooth.BluetoothError(e)
            if len(i) == 0:
                print("normal shutdown")
                break
                # Normal shutdown?
            while True:
                try:
                    self.clientSock.sendall(i)
                except BlockingIOError:
                    print("sending resource unavailable")
                    continue
                except bluetooth.BluetoothError as e:
                    if "Resource temporarily unavailable" in str(e):
                        print("sending BT resource unavailable")
                        continue
                    else:
                        raise bluetooth.BluetoothError(e)
                finally:
                    break

        self.othread.stop()
        self.stop()


class MyConnection:
    def __init__(self, serverSock, clientSock):
        # make calls non blocking
        serverSock.setblocking(0)
        clientSock.setblocking(0)

        self.IThread = StreamThread(serverSock, clientSock)
        self.OThread = StreamThread(clientSock, serverSock)

        self.IThread.setup(self.OThread)
        self.OThread.setup(self.IThread)

    def start(self):
        self.IThread.start()
        self.OThread.start()

    def join(self):
        self.IThread.join()
        self.OThread.join()

    def stop(self):
        self.IThread.stop()
        self.OThread.stop()

