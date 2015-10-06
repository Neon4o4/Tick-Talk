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

g_lLoopPyAudioObj = []


def GetOneFreeObj():
    return LoopPyAudioObj.ProvideOneFreeObj()


class LoopPyAudioObj(object):
    nCurPos = 0

    def __init__(self):
        global g_dRecord
        self.m_pOutputStream = PyAudio().open(
            format=g_dRecord['format'],
            channels=g_dRecord['channels'],
            rate=g_dRecord['rate'],
            frames_per_buffer=g_dRecord['frames_per_buffer'],
            output=True)
        self.m_bInUse = False
        global g_lLoopPyAudioObj
        g_lLoopPyAudioObj.append(self)

    @classmethod
    def Init(cls):
        for i in range(3):
            LoopPyAudioObj()

    @classmethod
    def ProvideOneFreeObj(cls):
        global g_lLoopPyAudioObj
        if g_lLoopPyAudioObj[LoopPyAudioObj.nCurPos].m_bInUse is False:
            g_lLoopPyAudioObj[LoopPyAudioObj.nCurPos].m_bInUse = True
            LoopPyAudioObj.nCurPos = (
                LoopPyAudioObj.nCurPos + 1) % len(g_lLoopPyAudioObj)
            return g_lLoopPyAudioObj[LoopPyAudioObj.nCurPos]
        else:
            pObj = LoopPyAudioObj()
            pObj.m_bInUse = True
            LoopPyAudioObj.nCurPos = 0
            return pObj

LoopPyAudioObj.Init()
