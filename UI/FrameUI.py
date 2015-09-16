#! /usr/bin/env python

# coding=uft-8

import wx
import sys


g_pFrame = None


def GetGlobalDialogPanel():
    global g_pFrame
    if g_pFrame:
        return g_pFrame
    else:
        g_pFrame = CFrame()
        pass


class CFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='TT', size=(300, 400))
        self.Bind(wx.EVT_CLOSE, self.OnClose, self)
        self.Init()
        self.Show()

    def OnClose(self, event):
        self.Destroy()
        sys.exit(0)

    def Init(self):
        pass


def main():
    app = wx.App()
    CFrame()
    app.MainLoop()

if __name__ == '__main__':
    main()
