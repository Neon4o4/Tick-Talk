#! /usr/bin/env python

# coding=uft-8

import lib.getAddress as getAddress

# IPV6 related
g_sIPV6Addr = getAddress.GetIPV6Address()
g_nIPV6Port = 60006
g_nIPV6VerifyPort = 60005

# IPV4 related
g_sIPV4Addr = getAddress.GetIPV4Address()
g_nIPV4Port = 40004
g_nIPV4VerifyPort = 40003

# VerifyServer
g_sVerifyServerIPV6Address = "::1"
# g_sVerifyServerIPV4Address = g_sIPV4Addr
g_sVerifyServerIPV4Address = '209.141.42.245'
g_nVerifyServerSpecialIPV6Port = 60004
g_nVerifyServerSpecialIPV4Port = 40002


if __name__ == '__main__':
    print "g_sIPV6Addr = ", g_sIPV6Addr
    print "g_nIPV6Port = ", g_nIPV6Port
    print "g_nIPV6VerifyPort = ", g_nIPV6VerifyPort
    print "g_sIPV4Addr = ", g_sIPV4Addr
    print "g_nIPV4Port = ", g_nIPV4Port
    print "g_nIPV4VerifyPort = ", g_nIPV4VerifyPort
