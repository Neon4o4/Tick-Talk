#! /usr/bin/env python

# coding=uft-8


def GetIPV6Address():
    from subprocess import Popen, PIPE
    from re import search
    from platform import system


    """
    This function will return your local machine's ipv6 address if it exits.
    If the local machine doesn't have a ipv6 address,then this function return None.
    This function use subprocess to execute command "ipconfig", then get the output
    and use regex to parse it ,trying to  find ipv6 address.
    """
    platform = system()
    if platform == "Windows":
        getIPV6_process = Popen("ipconfig", stdout=PIPE)
    else:
        getIPV6_process = Popen("ifconfig", stdout=PIPE)

    output = (getIPV6_process.stdout.read())
    ipv6_pattern='(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})'
    m = search(ipv6_pattern, str(output))
    if m is not None:
        return m.group()
    else:
        return None


def GetIPV4Address():
    from socket import gethostname, gethostbyname
    addr = gethostbyname(gethostname())
    if addr == "127.0.0.1":
        return None
    else:
        return addr


def main():
    print type(GetIPV4Address())
    print GetIPV4Address()
    print type(GetIPV6Address())
    print GetIPV6Address()


if __name__ == '__main__':
    main()
