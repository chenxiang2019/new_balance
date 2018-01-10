#!/usr/bin/env python
import sys
import struct
import argparse
import commands
from scapy.all import *

parser = argparse.ArgumentParser(description='Sender')
parser.add_argument('-p', '--port', help='target port', 
                    type=str, action="store", default='s1-eth1')
parser.add_argument('-n', '--num', help='total number', 
                    type=str, action="store", default='100')
args = parser.parse_args()

def main():
	iface = args.port
	num = int(args.num)
	for i in range(num):
		p = Ether(src="00:00:00:00:00:01", dst="00:00:00:00:00:02") / IP(src="10.0.0.1", dst="10.0.0.2") / UDP(dport=340) / "Nothing's Gonna Change My Love For You"
		sendp(p, iface = iface, verbose = 0)

if __name__ == '__main__':
	main()
