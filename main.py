#! /usr/bin/env python

# coding=uft-8

import threading
import Network.server
import Network.client
import UI.main


def main():
    Network.server.main()
    Network.client.main()
    UI.main.main()


if __name__ == '__main__':
    main()
    __MAIN__THREAD__LOCK__ = threading.Lock()
    __MAIN__THREAD__LOCK__.acquire()
    __MAIN__THREAD__LOCK__.acquire()
