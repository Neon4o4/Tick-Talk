#! /usr/bin/env python

# coding=uft-8

import socket
import threading
from lib.myTCPServer import ThreadedTCPServer, ThreadedTCPRequestHandler
import Defines.network
import Defines.verify
from copy import deepcopy


def _send_message_to_addr(res, sMessage):
    af, socktype, proto, cannoname, sa = res
    pSocket = socket.socket(af, socktype, proto)
    try:
        pSocket.connect(sa)
        pSocket.sendall(sMessage)
    except Exception:
        print 'Cannot send message or connect to server.\
            Please check verifyServer.py._send_message_to_addr.'
    pSocket.close()


class VerifyServerRequestHandler(ThreadedTCPRequestHandler):
    """
    Verify requests handler.
    """
    def handle(self):
        try:
            data = self.request.recv(16384)
        except Exception:
            print 'Cannot receive message.\
            Please check verifyServer.py.VerifyServerRequestHandler.handle 1.'
        hostname, res, loginorout = eval(data)
        try:
            self.request.sendall(str((0, Defines.verify.g_dUserDict)))
        except Exception:
            print 'Cannot send message.\
            Please check verifyServer.py.VerifyServerRequestHandler.handle 2.'
        if Defines.verify.g_pLock.accquire():
            if loginorout:
                Defines.verify.g_dUserDict[res] = hostname
            else:
                del Defines.verify.g_dUserDict[res]
            Defines.verify.g_nMessageID += 1
            curUserDict = deepcopy(Defines.verify.g_dUserDict)
            sendMessage = str((Defines.verify.g_nMessageID, curUserDict))
        Defines.verify.g_pLock.release()
        for addr in curUserDict.keys():
            t = threading.Thread(
                target=_send_message_to_addr, args=(addr, sendMessage))
            t.start()


def main():
    # Verify server
    res = socket.getaddrinfo(
        Defines.network.g_sIPV6Addr,
        Defines.network.g_nIPV6VerifyPort,
        socket.AF_INET6, socket.SOCK_STREAM, 0, socket.AI_PASSIVE)
    af, socktype, proto, cannoname, sa = res[0]
    server = ThreadedTCPServer(sa, VerifyServerRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()
    print "verifyServer_thread start"


if __name__ == '__main__':
        main()
        while True:
            pass
