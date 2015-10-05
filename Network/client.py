#! /usr/bin/env python

# coding=uft-8

import socket
from pyaudio import PyAudio, paInt16
import threading

from server import main
t = threading.Thread(target=main)
t.start()
