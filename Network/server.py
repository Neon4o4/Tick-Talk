#! /usr/bin/env python

# coding=uft-8

# Created by lixu19950414 and Neon404 on 2015/10/2

import socket
import threading
from SocketServer import BaseServer, BaseRequestHandler, ThreadingMixIn, TCPServer
import getAddress
from pyaudio import PyAudio, paInt16

bTest = False
g_sIPV4Addr = getAddress.GetIPV4Address()
g_nIPV4Port = 40004
g_sIPV6Addr = getAddress.GetIPV6Address()
g_nIPV6Port = 60006


class ThreadedTCPRequestHandler(BaseRequestHandler):
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
            cur_thread = threading.current_thread()
            # print cur_alive_thread_num
            s = 0
            for i in range(10000000):
                s += 1
            nThreadNum = threading.activeCount()
            response = "{}: {}".format(cur_thread.name, data) + "\nCurrent alive thread_num is " + str(nThreadNum)
            self.request.sendall(response)



class MyTCPServer(TCPServer):
    """
    Rewrite of TCPServer in order to support IPV6 network.
    Change BaseServer's __init__ method's server address to new form.
    Change TCPServer's socket to new type of socket using af, socktype, proto.
    """
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        """
        @prama server_address This prama shoubld be create by socket.getaddrinfo method.
        """
        BaseServer.__init__(self, server_address, RequestHandlerClass)
        global g_sIPV6Addr, g_nIPV6Port
        res = socket.getaddrinfo(
            g_sIPV6Addr, g_nIPV6Port, socket.AF_INET6,
            socket.SOCK_STREAM, 0, socket.AI_PASSIVE)
        af, socktype, proto, canonname, sa = res[0]
        self.socket = socket.socket(af, socktype, proto)
        if bind_and_activate:
            try:
                self.server_bind()
                self.server_activate()
            except:
                self.server_close()
                raise


class ThreadedTCPServer(ThreadingMixIn, MyTCPServer):
    """
    This is the mixture of MyTCPServer and ThreadingMixIn.
    This class inherits MyTCPServer's __init__ method.
    """


def main():
    global g_sIPV6Addr, g_nIPV6Port
    res = socket.getaddrinfo(
        g_sIPV6Addr, g_nIPV6Port, socket.AF_INET6,
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
        g_sIPV6Addr, g_nIPV6Port, socket.AF_INET6,
        socket.SOCK_STREAM, 0, socket.AI_PASSIVE)
    # print res
    af, socktype, proto, canonname, sa = res[0]
    server = ThreadedTCPServer(sa, ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print "Server loop starts!"
    while True:
        pass
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
