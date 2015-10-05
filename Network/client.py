#! /usr/bin/env python

# coding=uft-8

import socket
from pyaudio import PyAudio, paInt16
import threading
import json
from lib.myTCPServer import ThreadedTCPServer, ThreadedTCPRequestHandler
import Defines.verify
import Defines.network

# from server import main
# t = threading.Thread(target=main)
# t.start()


class ClientRequestHandler():
    """
    Designed for receive data stream.
    """
    def __init__(self, **RecorderConfig):
        self.config = {}
        if RecorderConfig['Recorder']:
            for key in RecorderConfig['Recorder']:
                self.config[key] = RecorderConfig[key]
            RecorderConfig.pop('Recorder')
        for key in ['rate', 'channels', 'format', 'frames_per_buffer']:
            if RecorderConfig[key]:
                self.config[key] = RecorderConfig[key]

    def _send_message_to_addr(addr, sMessage):
        af, socktype, proto, cannoname, sa = addr
        pSocket = socket.socket(af, socktype, proto)
        pSocket.connect(sa)
        pSocket.sendall(sMessage)
        pSocket.close()

    def handle(self):
        # almost done. Update&Sync of g_dUserDict is established in Server part
        # thus i didnt do it again
        # i think pPyAudioObj should be set as a global variable
        pPyAudioObj = PyAudio()
        pStream = pPyAudioObj.open(
            format=self.config['format'],
            channels=self.config['channels'],
            rate=self.config['rate'],
            frames_per_buffer=self.config['frames_per_buffer'],
            input=True)
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
                        target=ClientRequestHandler._send_message_to_addr,
                        args=(addr, data))
                    t.start()
                except Exception:
                    print 'Cannot receive data.\
                        Please check Network.server.ClientRequestHandler 2.'
        Defines.verify.g_pLock.release()
        pStream.close()

    def sendLoginVerifyMsg(self,):
        pass


def main():
    pass
