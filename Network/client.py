#! /usr/bin/env python

# coding=uft-8

import socket
from pyaudio import PyAudio
import threading
import Defines.verify
import Defines.network
import Defines.recorder
from copy import deepcopy
import weakref


g_wrpMsgSender = None


def _send_message_to_addr(res, sMessage):
    res = socket.getaddrinfo(
        res,
        Defines.network.g_nIPV4Port,
        socket.AF_INET,
        socket.SOCK_STREAM,
        0,
        socket.AI_PASSIVE)
    # print res
    af, socktype, proto, cannoname, sa = res[0]
    pSocket = socket.socket(af, socktype, proto)
    try:
        pSocket.connect(sa)
        pSocket.sendall(sMessage)
    except Exception:
        print 'Socket Exception happened in \
        client.py._send_message_to_addr'
    pSocket.close()


class MsgSender():
    """
    Designed for receive data stream.
    """
    def __init__(self, RecorderConfig):
        self.config = RecorderConfig
        self.pPyAudioObj = PyAudio()
        self.pStream = None

    def handle(self):
        if not self.pStream:
            self.pStream = self.pPyAudioObj.open(
                format=self.config['format'],
                channels=self.config['channels'],
                rate=self.config['rate'],
                frames_per_buffer=self.config['frames_per_buffer'],
                input=True)
        pStream = self.pStream
        try:
            data = pStream.read(self.config['bufferSize'])
        except Exception, e:
            print 'Cannot recognize read sound stream.\
                Please check Network.client.MsgSender 1.'
            print e
        # lock g_dUserDict
        if Defines.verify.g_pLock.acquire():
            UserDict = deepcopy(Defines.verify.g_dUserDict)
        Defines.verify.g_pLock.release()
        # print 'UserDict: %s' % str(UserDict)
        for addr in UserDict:
        # if addr != Defines.network.g_sIPV4Addr:
            try:
                t = threading.Thread(
                    target=_send_message_to_addr,
                    args=(addr, data))
                t.start()
            except Exception:
                print 'Cannot send data.\
                    Please check Network.client.MsgSender 2.'

    def sendLoginVerifyMsg(self, loginorout=True):
        sMessage = str((
            socket.gethostname(), Defines.network.g_sIPV4Addr, loginorout))
        res = socket.getaddrinfo(
            Defines.network.g_sVerifyServerIPV4Address,
            Defines.network.g_nVerifyServerSpecialIPV4Port,
            socket.AF_INET,
            socket.SOCK_STREAM,
            0,
            socket.AI_PASSIVE)
        af, socktype, proto, cannoname, sa = res[0]
        try:
            pSocket = socket.socket(af, socktype, proto)
            pSocket.connect(sa)
            pSocket.sendall(sMessage)
            pSocket.close()
        except Exception:
            print 'Fail when sending verify message.'

    def sendLoginOutVerifyMsg(self):
        self.sendLoginVerifyMsg(self, False)


def main():
    msgSender = MsgSender(Defines.recorder.g_dRecord)
    global g_wrpMsgSender
    g_wrpMsgSender = weakref.ref(msgSender)
    msgSender.sendLoginVerifyMsg()
    while True:
        msgSender.handle()

if __name__ == '__main__':
    main()
