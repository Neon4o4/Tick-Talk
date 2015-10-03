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
g_dConnected = {}  # This dictionary contains (hostname, (af, socktype, proto, canonname, sa)) as elements.
g_pLock = threading.Lock()


class ThreadedTCPRequestHandler(BaseRequestHandler):
    """
    Server's request handler.
    Rewrite method 'handle' to fix recv and send/sendall issues.
    """
    def handle(self):
        data = self.request.recv(1024)
        hostname = data
        self.request.sendall('hostname: %s is trying to connect', hostname)  # Send hostname back.
        data = self.request.recv(1024)
        res = eval(data)
        self.request.sendall('using address: %s', data)  # Send address back.
        global g_pLock
        if g_pLock.acquire():
            g_dConnected[hostname] = res
        g_pLock.release()



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
