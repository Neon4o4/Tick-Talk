#! /usr/bin/env python

# coding=uft-8

import threading
import Network.server
import Network.client
import UI.main


def main():
    t1 = threading.Thread(target=Network.server.main)
    t1.start()
    t2 = threading.Thread(target=Network.client.main)
    t2.start()
    t3 = threading.Thread(target=UI.main.main)
    t3.start()


if __name__ == '__main__':
    main()
    # while True:
    #     order = raw_input("Please enter an order: ")
    #     if order == "exit":
    #         from Network.server import g_wrpServerReceive, g_wrpServerVerify
    #         from Network.client import g_wrpMsgSender
    #         g_wrpMsgSender().sendLoginOutVerifyMsg()
    #         g_wrpServerReceive().shutdown()
    #         g_wrpServerReceive().server_close()
    #         g_wrpServerVerify().shutdown()
    #         g_wrpServerVerify().server_close()
    #         break
    # import sys
    # sys.exit(0)
    __MAIN__THREAD__LOCK__ = threading.Lock()
    __MAIN__THREAD__LOCK__.acquire()
    __MAIN__THREAD__LOCK__.acquire()
