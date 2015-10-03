#! /usr/bin/env python

# coding=uft-8

from lib.myTCPServer import MyTCPServer
import socket
import threading
from SocketServer import BaseServer, BaseRequestHandler, ThreadingMixIn
import Defines.network as network


g_sIPV4Addr = network.g_sIPV4
g_nIPV4Port = network.g_nIPV4Port
g_sIPV6Addr = network.g_sIPV6
g_nIPV6Port = network.g_nIPV6Port
g_lConnected = {}  # This dictionary contains (hostname, (af, socktype, proto, canonname, sa)) as elements.


class ThreadedTCPRequestHandler(BaseRequestHandler):
    """
    Server's request handler.
    Rewrite method 'handle' to fix recv and send/sendall issues.
    """
    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        # print cur_alive_thread_num
        s = 0
        for i in range(10000000):
            s += 1
        nThreadNum = threading.activeCount()
        response = "{}: {}".format(cur_thread.name, data) + "\nCurrent alive thread_num is " + str(nThreadNum)
        self.request.sendall(response)


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
    print "verifyServer loop starts!"
    # server.shutdown()
    # server.server_close()
