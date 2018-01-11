#!/usr/bin/env python

import struct
import sys
import argparse
import commands
from time import sleep

parser = argparse.ArgumentParser(description='SDN & P4 Demo')
parser.add_argument('-p', '--thrift_port', help='Thrift Port',
                    type=int, action="store", default=1)
args = parser.parse_args()

def read_counter():
	thrift_port = args.thrift_port

	"""read counter"""
        cmd = "sudo ./read_counter.sh %d > pkt_number.txt" % thrift_port
        status, output = commands.getstatusoutput(cmd)
        if status != 0:
                print "\nError: counter cannot be read!\n"
		return
	
	pkt_number, pkt_bytes = 0, 0
	"""return counter number"""
	with open("pkt_number.txt", "r") as f:
		vals = []
		for line in f:
			if not f: break
			vals = line.split()
			if vals[0] != "RuntimeCmd:":
				continue
			else:
				break
		raw_str1, raw_str2 = vals[-2], vals[-1]
		pkt_number = int(raw_str1.split('=')[-1][:-1])
		pkt_bytes = int(raw_str2.split('=')[-1][:-1])

	"""delete tmp file"""
	cmd = "sudo rm -rf pkt_number.txt"
        status, output = commands.getstatusoutput(cmd)
        if status != 0:
                print "\nError: cannot delete pkt_number.txt!\n"
                return

	return pkt_number, pkt_bytes

if __name__ == '__main__':
	read_counter()

