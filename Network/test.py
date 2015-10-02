import socket
import threading


class CTest(object):
    def __init__(self, res, message):
        self.res = res
        # af, socktype, proto, canonname, sa = res
        # self.m_pSocket = socket.socket(af, socktype, proto)
        self.m_sMessage = message

    def Send(self):
        af, socktype, proto, canonname, sa = self.res
        pSocket = socket.socket(af, socktype, proto)
        pSocket.connect(sa)
        pSocket.sendall(self.m_sMessage)
        response = pSocket.recv(1024)
        print "Received: {}".format(response)
        pSocket.close()

    # def Close(self):
    #     self.m_pSocket.close()


def create_CTest():
    res = (30, 1, 6, '', ('2001:250:401:3517:a65e:60ff:febd:e96f', 60006, 0, 0))
    # print message
    p = CTest(res, "1")
    p.Send()


def main():
    for i in range(5):
        t = threading.Thread(target=create_CTest)
        t.start()

if __name__ == '__main__':
    main()
