#!/usr/bin/env python

import os
import random
import struct
import sys
import argparse
import commands
from time import sleep
from read_counter import *
from scripts.definitions import *

parser = argparse.ArgumentParser(description='SDN & P4 Demo')
parser.add_argument('-p', '--packets', help='threshold: packet/s',
                    type=int, action="store", default=100)
args = parser.parse_args()

thrift_base = 22222
l2_sw_ports = [22223, 22226]
l3_sw_ports = [22224, 22225]

paths = [[2,3],[2,3],[2,4],[2,4],[5,3],[5,3],[5,4],[5,4]]

def reset_all_counters(swnum=5):
	for i in range(swnum):
		cmd = "sudo ./reset_counter.sh %d" % (i+thrift_base)
                status, output = commands.getstatusoutput(cmd)
                if status != 0:
                        print "Error: cannot reset counter of sw%d" % (i+1)
                        return

def main():
	global CURRENT_L2_SW
	global CURRENT_L3_SW
	tgtl2sw = [2,5]
	tgtl3sw = [3,4]
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
	
	if flag1 == False and flag2 == False:
		reset_all_counters()
		return

	tgtl2sw.remove(l2swid)
	tgtl3sw.remove(l3swid)

	newPath = []

	# if both l2 and l3 exceed the threshold
	if flag1 == True and flag2 == True:
		newl2sw_idx = random.randint(0, len(tgtl2sw)-1)
		newl2sw = tgtl2sw[newl2sw_idx]
		newl3sw_idx = random.randint(0, len(tgtl3sw)-1)
		newl3sw = tgtl3sw[newl3sw_idx]

		newPath.append(newl2sw)
		newPath.append(newl3sw)
		newPathID = paths.index(newPath)+1

		# set new paths
		cmd = "sudo ./set_path.py -p %d" % (newPathID)
		status, output = commands.getstatusoutput(cmd)
		if status != 0:
			print "Error: cannot set new path"
			return
		print "Set new path successfully! PathID:%d" % newPathID

		# update current switches
		CURRENT_L2_SW, CURRENT_L3_SW = newl2sw, newl3sw

		# reset counters 
		reset_all_counters()

	elif flag1 == True and flag2 == False:
		newl2sw_idx = random.randint(0, len(tgtl2sw)-1)
                newl2sw = tgtl2sw[newl2sw_idx]
                newl3sw = CURRENT_L3_SW

                newPath.append(newl2sw)
                newPath.append(newl3sw)
                newPathID = paths.index(newPath)+1

                cmd = "sudo ./set_path.py -p %d" % (newPathID)
                status, output = commands.getstatusoutput(cmd)
                if status != 0:
                        print "Error: cannot set new path"
                        return
                print "Set new path successfully! PathID:%d" % newPathID

		CURRENT_L2_SW, CURRENT_L3_SW = newl2sw, newl3sw

		# reset counters 
		reset_all_counters()

	elif flag1 == False and flag2 == True:
                newl2sw = CURRENT_L2_SW
                newl3sw_idx = random.randint(0, len(tgtl3sw)-1)
                newl3sw = tgtl3sw[newl3sw_idx]

                newPath.append(newl2sw)
                newPath.append(newl3sw)
                newPathID = paths.index(newPath)+1

                cmd = "sudo ./set_path.py -p %d" % (newPathID)
                status, output = commands.getstatusoutput(cmd)
                if status != 0:
                        print "Error: cannot set new path"
                        return
                print "Set new path successfully! PathID:%d" % newPathID

                CURRENT_L2_SW, CURRENT_L3_SW = newl2sw, newl3sw

		# reset counters 
		reset_all_counters()

	else:
		reset_all_counters()

if __name__ == '__main__':
    try:
        while True: 
		main()
		sleep(1)
    except KeyboardInterrupt:
        print 'User Interrupted'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
