#! /usr/bin/env python

# coding=uft-8

g_dUserDict = {}
g_dVerifyServerUserDict = {}
g_nMessageID = 0

import threading
g_pLock = threading.Lock()
g_pVerifyServerLock = threading.Lock()
