#!/usr/bin/env python

import struct
import sys
import argparse
import commands
from time import sleep
from read_counter import *

parser = argparse.ArgumentParser(description='SDN & P4 Demo')
parser.add_argument('-p', '--packets', help='packet threshold',
                    type=int, action="store", default=1)
args = parser.parse_args()

thrift_base = 22222
l2_sw_ports = [22223, 22226]
l3_sw_ports = [22224, 22225]

def main():
	# threshold
	threshold = args.packets
	# path in terms of switch id
	l2swid, l3swid = 2, 3
	# is over the threshold?	
	flag1, flag2 = False, False	

	# query l2 switches
	for port in l2_sw_ports:
		l2swid = port-thrift_base+1
		pkt_number, pkt_bytes = read_counter(port)
		if pkt_number > threshold:
			flag1 = True
			break

	# query l3 switches
        for port in l3_sw_ports:
                l3swid = port-thrift_base+1
                pkt_number, pkt_bytes = read_counter(port)
                if pkt_number > threshold:
                        flag2 = True
                        break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print 'Interrupted'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
