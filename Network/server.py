#! /usr/bin/env python

# coding=uft-8

import socket
import threading
from pyaudio import PyAudio
from lib.myTCPServer import ThreadedTCPServer, ThreadedTCPRequestHandler
import Defines.network
import Defines.verify
import Defines.recorder
import weakref
import Defines.loopPyAudioObject


g_wrpServerVerify = None
g_wrpServerReceive = None


class ServerReceiveRequestHandler(ThreadedTCPRequestHandler):
    """
    Designed for receive data stream.
    """
    def handle(self):
        try:
            data = self.request.recv(16384)
        except Exception:
            print 'Cannot receive data.\
                Please check Network.server.ServerReceiveRequestHandler 1.'
        try:
            pObj = Defines.loopPyAudioObject.GetOneFreeObj()
            pStream = pObj.m_pOutputStream
            pStream.write(data)
        except Exception, e:
            print 'Cannot recognize received sound stream.\
                Please check Network.server.ServerReceiveRequestHandler 2.'
            print e
        finally:
            pObj.m_bInUse = False


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
        Defines.network.g_sIPV4Addr, Defines.network.g_nIPV4VerifyPort,
        socket.AF_INET, socket.SOCK_STREAM, 0, socket.AI_PASSIVE)
    verifyAf, verifySocktype, verifyProto,\
        verifyCanonname, verifySa = verifyRes[0]
    serverVerify = ThreadedTCPServer(verifySa, ServerVerifyRequestHandler)
    global g_wrpServerVerify
    g_wrpServerVerify = weakref.ref(serverVerify)
    serverVerify_thread = threading.Thread(target=serverVerify.serve_forever)
    serverVerify_thread.setDaemon(True)
    serverVerify_thread.start()
    print 'serverVerify_thread start'

    # Receive port
    receiveRes = socket.getaddrinfo(
        Defines.network.g_sIPV4Addr, Defines.network.g_nIPV4Port,
        socket.AF_INET, socket.SOCK_STREAM, 0, socket.AI_PASSIVE)
    receiveAf, receiveSocktype, receiveproto,\
        receiveCanonname, receiveSa = receiveRes[0]
    # print receiveSa
    # receiveSa[0] = ''
    serverReceive = ThreadedTCPServer(receiveSa, ServerReceiveRequestHandler)
    global g_wrpServerReceive
    g_wrpServerReceive = weakref.ref(serverReceive)
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
