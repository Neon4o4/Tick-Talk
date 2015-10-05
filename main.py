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
    __MAIN__THREAD__LOCK__ = threading.Lock()
    __MAIN__THREAD__LOCK__.acquire()
    __MAIN__THREAD__LOCK__.acquire()
