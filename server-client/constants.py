"""
    This file is the constants of the peer to peer network
"""

import socket 
import threading 
import sys
import time
from random import randint

import fileIO

BYTE_SIZE = 2048
HOST = '192.168.1.203'
#HOST = '127.0.0.1'
PORT = 5000
PEER_BYTE_DIFFERENTIATOR = b'\x11' 
RAND_TIME_START = 1
RAND_TIME_END = 2
REQUEST_STRING = "req"
