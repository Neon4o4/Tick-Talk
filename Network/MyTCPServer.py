#! /usr/bin/env python

# coding=uft-8

from SocketServer import TCPServer, BaseServer
import socket


class MyTCPServer(TCPServer):
    """
    Rewrite of TCPServer in order to support IPV6 network.
    Change BaseServer's __init__ method's server address to new form.
    Change TCPServer's socket to new type of socket using af, socktype, proto.
    """
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        """
        @prama server_address This prama shoubld be create by socket.getaddrinfo method.
        """
        BaseServer.__init__(self, server_address, RequestHandlerClass)
        global g_sIPV6Addr, g_nIPV6Port
        res = socket.getaddrinfo(
            server_address[0], server_address[1], socket.AF_INET6,
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
