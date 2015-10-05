#! /usr/bin/env python

# coding=uft-8

from pyaudio import paInt16

g_dRecord = {
    "format": paInt16,
    "channels": 1,
    "rate": 16000,
    "frames_per_buffer": 2000,
    "bufferSize": 2000
}
