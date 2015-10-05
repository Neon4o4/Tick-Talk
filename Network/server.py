#! /usr/bin/env python

# coding=uft-8

import socket
import threading
from pyaudio import PyAudio
from lib.myTCPServer import ThreadedTCPServer, ThreadedTCPRequestHandler
import Defines.network
import Defines.verify
import Defines.recorder


class ServerReceiveRequestHandler(ThreadedTCPRequestHandler):
    """
    Designed for receive data stream.
    """
    def handle(self):
        pPyAudioObj = PyAudio()
        pStream = pPyAudioObj.open(
            format=Defines.recorder.g_dRecord['format'],
            channels=Defines.recorder.g_dRecord['channels'],
            rate=Defines.recorder.g_dRecord['rate'],
            frames_per_buffer=Defines.recorder.g_dRecord['frames_per_buffer'],
            output=True)
        try:
            data = self.request.recv(16384)
        except Exception:
            print 'Cannot receive data.\
                Please check Network.server.ServerReceiveRequestHandler 1.'
        try:
            pStream.write(data)
        except Exception:
            print 'Cannot recognize received sound stream.\
                Please check Network.server.ServerReceiveRequestHandler 2.'
        pStream.close()


class ServerVerifyRequestHandler(ThreadedTCPRequestHandler):
    """
    Designed for server verify.
    """
    def handle(self):
        try:
            data = self.request.recv(16384)
            messageID, userDict = eval(data)
            if Defines.verify.g_pLock.acquire():
                if messageID > Defines.verify.g_nMessageID:
                    Defines.verify.g_dUserDict = userDict
                    Defines.verify.g_nMessageID = messageID
            Defines.verify.g_pLock.release()
        except Exception:
            print 'Cannot receive data.\
            Please check Network.server.ServerVerifyRequestHandler'


def main():
    # Verify port
    verifyRes = socket.getaddrinfo(
        Defines.network.g_sIPV6Addr, Defines.network.g_nIPV6VerifyPort,
        socket.AF_INET6, socket.SOCK_STREAM, 0, socket.AI_PASSIVE)
    verifyAf, verifySocktype, verifyProto,\
        verifyCanonname, verifySa = verifyRes[0]
    serverVerify = ThreadedTCPServer(verifySa, ServerVerifyRequestHandler)
    serverVerify_thread = threading.Thread(target=serverVerify.serve_forever)
    serverVerify_thread.setDaemon(True)
    serverVerify_thread.start()
    print 'serverVerify_thread start'

    # Receive port
    receiveRes = socket.getaddrinfo(
        Defines.network.g_sIPV6Addr, Defines.network.g_nIPV6Port,
        socket.AF_INET6, socket.SOCK_STREAM, 0, socket.AI_PASSIVE)
    receiveAf, receiveSocktype, receiveproto,\
        receiveCanonname, receiveSa = receiveRes[0]
    serverReceive = ThreadedTCPServer(receiveSa, ServerReceiveRequestHandler)
    serverReceive_thread = threading.Thread(target=serverReceive.serve_forever)
    serverReceive_thread.setDaemon(True)
    serverReceive_thread.start()
    print 'serverReceive_thread start'
    num_alive_thread = threading.activeCount()
    print 'Current active thread num is: ', num_alive_thread

if __name__ == '__main__':
    main()
    __MAIN__THREAD__LOCK__ = threading.Lock()
    __MAIN__THREAD__LOCK__.acquire()
    __MAIN__THREAD__LOCK__.acquire()
