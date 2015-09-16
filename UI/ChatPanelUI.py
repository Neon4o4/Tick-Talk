#! /usr/bin/env python

# coding=uft-8

import wx
from weakref import ref


g_pChatPanel = None


def GetGlobalChatPanel():
    global g_pChatPanel
    if g_pChatPanel:
        return g_pChatPanel
    else:
        import FrameUI
        g_pChatPanel = CChatPanel(FrameUI.g_pFrame)


class CChatPanel(wx.Panel):
    def __init__(self, pParent):
        wx.Panel.__init__(self, pParent)
        self.wrpFrame = ref(pParent, self.DestroyDialog)
        self.Init()

    def DestroyDialog(self):
        global g_pChatPanel
        g_pChatPanel = None

    def Init(self):
        # Tags
        pStaticText = wx.StaticText(self, 1, u"测试")
        pStaticText.SetPosition(wx.Point(100, 100))
        self.pText1 = pStaticText
