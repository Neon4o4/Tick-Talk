#! /usr/bin/env python

# coding=uft-8

import socket
from pyaudio import PyAudio
import threading
import Defines.verify
import Defines.network
import Defines.recorder
from copy import deepcopy


def _send_message_to_addr(res, sMessage):
    res = socket.getaddrinfo(
        res,
        Defines.network.g_nIPV4Port,
        socket.AF_INET,
        socket.SOCK_STREAM,
        0,
        socket.AI_PASSIVE)
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
        print 111
        if not self.pStream:
            self.pStream = self.pPyAudioObj.open(
                format=self.config['format'],
                channels=self.config['channels'],
                rate=self.config['rate'],
                frames_per_buffer=self.config['frames_per_buffer'],
                input=True)
        pStream = self.pStream
        try:
            print 222
            data = pStream.read(self.config['bufferSize'])
            print 333
        except Exception, e:
            print 'Cannot recognize received sound stream.\
                Please check Network.server.ClientRequestHandler 1.'
            print e
        # lock g_dUserDict
        UserDict = deepcopy(Defines.verify.g_dUserDict)
        print 'UserDict: %s' % str(UserDict)
        for addr in UserDict:
            try:
                t = threading.Thread(
                    target=MsgSender._send_message_to_addr,
                    args=(addr, data))
                t.start()
                print 'thread start'
            except Exception:
                print 'Cannot receive data.\
                    Please check Network.server.ClientRequestHandler 2.'

    def sendLoginVerifyMsg(self):
        sMessage = str((
            socket.gethostname(), Defines.network.g_sIPV4Addr, True))
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


def main():
    msgSender = MsgSender(Defines.recorder.g_dRecord)
    msgSender.sendLoginVerifyMsg()
    while True:
        msgSender.handle()

if __name__ == '__main__':
    main()
