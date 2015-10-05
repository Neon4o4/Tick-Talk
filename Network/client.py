#! /usr/bin/env python

# coding=uft-8

import socket
from pyaudio import PyAudio
import threading
import Defines.verify
import Defines.network
import Defines.recorder


class MsgSender():
    """
    Designed for receive data stream.
    """
    def __init__(self, RecorderConfig):
        self.config = RecorderConfig
        self.pPyAudioObj = PyAudio()
        self.pStream = self.pPyAudioObj.open(
            format=self.config['format'],
            channels=self.config['channels'],
            rate=self.config['rate'],
            frames_per_buffer=self.config['frames_per_buffer'],
            input=True)

    def _send_message_to_addr(addr, sMessage):
        af, socktype, proto, cannoname, sa = addr
        pSocket = socket.socket(af, socktype, proto)
        pSocket.connect(sa)
        pSocket.sendall(sMessage)
        pSocket.close()

    def handle(self):
        pStream = self.pStream
        try:
            data = pStream.read(self.config['bufferSize'])
        except Exception:
            print 'Cannot recognize received sound stream.\
                Please check Network.server.ClientRequestHandler 1.'
        # lock g_dUserDict
        if Defines.verify.g_pLock.acquire():
            for addr in Defines.verify.g_dUserDict:
                try:
                    t = threading.Thread(
                        target=MsgSender._send_message_to_addr,
                        args=(addr, data))
                    t.start()
                except Exception:
                    print 'Cannot receive data.\
                        Please check Network.server.ClientRequestHandler 2.'
        Defines.verify.g_pLock.release()

    def sendLoginVerifyMsg(self):
        verifyIP = Defines.network.g_sIPV6Addr
        verifyPort = Defines.network.g_nIPV6VerifyPort
        res = socket.getaddrinfo(
            verifyIP,
            verifyPort,
            socket.AF_INET6,
            socket.SOCK_STREAM,
            0,
            socket.AI_PASSIVE)
        sMessage = str((socket.gethostname(), res[0], True))
        af, socktype, proto, cannoname, sa = res[0]
        pSocket = socket.socket(af, socktype, proto)
        pSocket.connect(sa)
        pSocket.sendall(sMessage)
        pSocket.close()


def main():
    msgSender = MsgSender(Defines.recorder.g_dRecord)
    msgSender.sendLoginVerifyMsg()
    while True:
        msgSender.handle()

if __name__ == '__main__':
    main()
