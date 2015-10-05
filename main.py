#! /usr/bin/env python

# coding=uft-8

import Network.server
import Network.client
import UI.main


def main():
    Network.server.main()
    Network.client.main()
    UI.main.main()


if __name__ == '__main__':
    main()
    while True:
        pass
