#! /usr/bin/env python

# coding=uft-8

from pyaudio import PyAudio, paInt16

g_dRecord = {
    "format": paInt16,
    "channels": 1,
    "rate": 16000,
    "frames_per_buffer": 2000,
    "bufferSize": 2000
}

g_pOutputStream = PyAudio().open(
    format=g_dRecord['format'],
    channels=g_dRecord['channels'],
    rate=g_dRecord['rate'],
    frames_per_buffer=g_dRecord['frames_per_buffer'],
    output=True)
