#! /usr/bin/env python

# coding=uft-8

from lib.myTCPServer import ThreadedTCPServer, ThreadedTCPRequestHandler
import socket
import threading
import Defines.network as network


g_sIPV4Addr = network.g_sIPV4
g_nIPV4Port = network.g_nIPV4Port
g_sIPV6Addr = network.g_sIPV6
g_nIPV6Port = network.g_nIPV6Port
g_dConnected = {}  # This dictionary contains ((af, socktype, proto, canonname, sa): hostname) as elements.
g_pLock = threading.Lock()


def SendMessage(res, message):
    af, socktype, proto, canonname, sa = res
    pSocket = socket.socket(af, socktype, proto)
    pSocket.connect(sa)
    pSocket.sendall(message)
    pSocket.close()


class VerifyServerRequestHandler(ThreadedTCPRequestHandler):
    nMessageID = 0
    """
    Server's request handler.
    Rewrite method 'handle' to fix recv and send/sendall issues.
    """
    def handle(self):
        data = self.request.recv(1024)
        hostname, res, loginorout = eval(data)
        global g_pLock, g_dConnected
        if g_pLock.acquire():
            VerifyServerRequestHandler.nMessageID += 1
            if loginorout is True:
                g_dConnected[res] = hostname  # In case same hostname.
            else:
                del g_dConnected[res]
            sSend = str(VerifyServerRequestHandler.nMessageID) + str(g_dConnected)
        g_pLock.release()
        for addr in g_dConnected.keys():
            t = threading.Thread(target=SendMessage, args=(addr, sSend))
            t.start()


def main():
    global g_sIPV6Addr, g_nIPV6Port
    res = socket.getaddrinfo(
        g_sIPV6Addr, g_nIPV6Port, socket.AF_INET6,
        socket.SOCK_STREAM, 0, socket.AI_PASSIVE)
    af, socktype, proto, canonname, sa = res[0]
    server = ThreadedTCPServer(sa, VerifyServerRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print "verifyServer loop starts!"
    while True:
        pass
    # server.shutdown()
    # server.server_close()
