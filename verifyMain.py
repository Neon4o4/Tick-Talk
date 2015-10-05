#! /usr/bin/env python

# coding=uft-8

import Verify.verifyServer
import threading


def main():
    Verify.verifyServer.main()

if __name__ == '__main__':
    main()
    __MAIN__THREAD__LOCK__ = threading.Lock()
    __MAIN__THREAD__LOCK__.acquire()
    __MAIN__THREAD__LOCK__.acquire()
