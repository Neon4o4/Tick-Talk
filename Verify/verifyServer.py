#! /usr/bin/env python

# coding=uft-8

import socket
import threading
from lib.myTCPServer import ThreadedTCPServer, ThreadedTCPRequestHandler
import Defines.network
import Defines.verify
from copy import deepcopy


def _send_message_to_addr(res, sMessage):
    res = socket.getaddrinfo(
        res,
        Defines.network.g_nIPV4VerifyPort,
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
        verifyServer.py._send_message_to_addr'
    pSocket.close()


class VerifyServerRequestHandler(ThreadedTCPRequestHandler):
    """
    Verify requests handler.
    """
    def handle(self):
        data = self.request.recv(16384)
        print "data: %s" % data
        hostname, res, loginorout = eval(data)
        print 111
        if Defines.verify.g_pVerifyServerLock.acquire():
            if loginorout:
                Defines.verify.g_dVerifyServerUserDict[res] = hostname
            else:
                del Defines.verify.g_dVerifyServerUserDict[res]
            Defines.verify.g_nMessageID += 1
            curUserDict = deepcopy(Defines.verify.g_dVerifyServerUserDict)
            sendMessage = str((Defines.verify.g_nMessageID, curUserDict))
        Defines.verify.g_pVerifyServerLock.release()
        print Defines.verify.g_dVerifyServerUserDict
        for addr in curUserDict.keys():
            t = threading.Thread(
                target=_send_message_to_addr, args=(addr, sendMessage))
            t.start()


def main():
    # Verify server
    res = socket.getaddrinfo(
        Defines.network.g_sIPV4Addr,
        Defines.network.g_nVerifyServerSpecialIPV4Port,
        socket.AF_INET, socket.SOCK_STREAM, 0, socket.AI_PASSIVE)
    af, socktype, proto, cannoname, sa = res[0]
    server = ThreadedTCPServer(sa, VerifyServerRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()
    print "verifyServer_thread start"


if __name__ == '__main__':
        main()
        __MAIN__THREAD__LOCK__ = threading.Lock()
        __MAIN__THREAD__LOCK__.acquire()
        __MAIN__THREAD__LOCK__.acquire()
