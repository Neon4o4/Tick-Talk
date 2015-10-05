#! /usr/bin/env python

# coding=uft-8

import socket
import threading
from pyaudio import PyAudio, paInt16
from lib.myTCPServer import ThreadedTCPServer, ThreadedTCPRequestHandler
from Defines.network import g_sIPV6Addr
from Defines.network import g_nIPV6Port
from Defines.network import g_nIPV6VerifyPort


class ServerReceiveRequestHandler(ThreadedTCPRequestHandler):
    """
    Designed for receive data stream.
    """
    def handle(self):
        pass


class ServerVerifyRequestHandler(ThreadedTCPRequestHandler):
    """
    Designed for server verify.
    """
    def handle(self):
        pass


def main():
    # Verify port
    verifyRes = socket.getaddrinfo(
        g_sIPV6Addr, g_nIPV6VerifyPort, socket.AF_INET6,
        socket.SOCK_STREAM, 0, socket.AI_PASSIVE)
    verifyAf, verifySocktype, verifyProto, verifyCanonname, verifySa = verifyRes[0]
    serverVerify = ThreadedTCPServer(verifySa, ServerVerifyRequestHandler)
    serverVerify_thread = threading.Thread(target=serverVerify.serve_forever)
    serverVerify_thread.setDaemon(True)
    serverVerify_thread.start()
    print 'serverVerify_thread start'

    # Receive port
    receiveRes = socket.getaddrinfo(
        g_sIPV6Addr, g_nIPV6Port, socket.AF_INET6,
        socket.SOCK_STREAM, 0, socket.AI_PASSIVE)
    receiveAf, receiveSocktype, receiveproto, receiveCanonname, receiveSa = receiveRes[0]
    serverReceive = ThreadedTCPServer(receiveSa, ServerReceiveRequestHandler)
    serverReceive_thread = threading.Thread(target=serverReceive.serve_forever)
    serverReceive_thread.setDaemon(True)
    serverReceive_thread.start()
    print 'serverReceive_thread start'

    while True:
        pass

if __name__ == '__main__':
    main()
