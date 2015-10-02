#! /usr/bin/env python

# coding=uft-8

import socket
import threading
from SocketServer import BaseServer, BaseRequestHandler, ThreadingMixIn, TCPServer
import getAddress
from pyaudio import PyAudio, paInt16

g_sIPV4Addr = getAddress.GetIPV4Address()
g_nIPV4Port = 40004
g_sIPV6Addr = getAddress.GetIPV6Address()
g_nIPV6Port = 60006


class ThreadedTCPRequestHandler(BaseRequestHandler):
    def handle(self):
        pPyAudioObj = PyAudio()
        pStream = pPyAudioObj.open(
            format=paInt16, channels=1, rate=16000, output=True)
        while True:
            data = self.request.recv(16384)
            pStream.write(data)


class MyTCPServer(TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
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
    pass


def main():
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


if __name__ == '__main__':
    main()
