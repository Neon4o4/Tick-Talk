#! /usr/bin/env python

# coding=uft-8

import socket
import threading
from pyaudio import PyAudio, paInt16
from lib.myTCPServer import ThreadedTCPServer, ThreadedTCPRequestHandler
from Defines.network import g_sIPV6Addr as g_sIPV6Addr
from Defines.network import g_nIPV6Port as g_nIPV6Port


bTest = True

g_pLock = threading.Lock()


class ServerRequestHandler(ThreadedTCPRequestHandler):
    """
    Server's request handler.
    Rewrite method 'handle' to fix recv and send/sendall issues.
    """
    def handle(self):
        if bTest is False:
            pPyAudioObj = PyAudio()
            pStream = pPyAudioObj.open(
                format=paInt16, channels=1, rate=16000, output=True)
            data = self.request.recv(16384)
            pStream.write(data)
        else:
            data = self.request.recv(1024)
            global g_pLock
            if g_pLock.acquire():
                cur_thread = threading.current_thread()
            g_pLock.release()
            # print cur_alive_thread_num
            s = 0
            for i in range(10000000):
                s += 1
            nThreadNum = threading.activeCount()
            response = "{}: {}".format(cur_thread.name, data) \
                + "\nCurrent alive thread_num is " + str(nThreadNum)
            self.request.sendall(response)


def main():
    global g_sIPV6Addr, g_nIPV6Port
    res = socket.getaddrinfo(
        g_sIPV6Addr, g_nIPV6Port, socket.AF_INET,
        socket.SOCK_STREAM, 0, socket.AI_PASSIVE)
    af, socktype, proto, canonname, sa = res[0]
    server = ThreadedTCPServer(sa, ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print "Server loop starts!"
    # server.shutdown()
    # server.server_close()


def test():
    """
    This method works with test.py in folder Network.
    """
    global g_sIPV6Addr, g_nIPV6Port, bTest
    bTest = True
    res = socket.getaddrinfo(
        g_sIPV6Addr, g_nIPV6Port, socket.AF_INET,
        socket.SOCK_STREAM, 0, socket.AI_PASSIVE)
    # print res
    af, socktype, proto, canonname, sa = res[0]
    server = ThreadedTCPServer(sa, ServerRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print "Server loop starts!"
    # p1 = CTest(res[0], "1")
    # p2 = CTest(res[0], "2")
    # p3 = CTest(res[0], "3")
    # from Utilities.Util import Functor
    # import time
    # time.sleep(3)
    # server.shutdown()
    # server.server_close()


if __name__ == '__main__':
    # main()
    test()
    pLock = threading.Lock()
    pLock.acquire()
    pLock.acquire()
