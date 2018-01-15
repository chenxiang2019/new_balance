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
parser.add_argument('-i', '--interval', help='inspection time interval/s',
                    type=int, action="store", default=3)
args = parser.parse_args()

thrift_base = 22222
l2_sw_ports = [22223, 22226]
l3_sw_ports = [22224, 22225]

paths = [[2,3],[2,3],[2,4],[2,4],[5,3],[5,3],[5,4],[5,4]]

swid_paths = ["NAN", "s1-s2-s3-h5", "s1-s2-s3-h4", 
              "s1-s2-s4-h3", "s1-s2-s4-h2",
              "s1-s5-s3-h5", "s1-s5-s3-h4",
              "s1-s5-s4-h3", "s1-s5-s4-h2"]

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

	# overhead swid
	l2_overhead, l3_overhead = [], []

	# query l2 switches
	for port in l2_sw_ports:
		l2swid = port-thrift_base+1
		pkt_number, pkt_bytes = read_counter(port)
		if pkt_number > threshold:
			flag1 = True
			l2_overhead.append(l2swid)

	# query l3 switches
        for port in l3_sw_ports:
                l3swid = port-thrift_base+1
                pkt_number, pkt_bytes = read_counter(port)
                if pkt_number > threshold:
                        flag2 = True
                        l3_overhead.append(l3swid)
	
	if flag1 == False and flag2 == False:
		reset_all_counters()
		return

	for i in l2_overhead:
		tgtl2sw.remove(i)
	for i in l3_overhead:
		tgtl3sw.remove(i)

	newPath = []

	# if both l2 and l3 exceed the threshold
	if flag1 == True and flag2 == True:
		for i in l2_overhead:
			print "Warnning: l2 s%d exceeds the threshold!" % i
		for i in l3_overhead:
			print "Warnning: l3 s%d exceeds the threshold!" % i

		newl2sw_idx = random.randint(0, len(tgtl2sw)-1)
		newl2sw = tgtl2sw[newl2sw_idx]
		newl3sw_idx = random.randint(0, len(tgtl3sw)-1)
		newl3sw = tgtl3sw[newl3sw_idx]

		newPath.append(newl2sw)
		newPath.append(newl3sw)

		newPathID, newPathIDList = -1, []
		for item in enumerate(paths):
			if item[1] == newPath:
				newPathIDList.append(item[0]+1)
				print "Find an avaliable path:", swid_paths[item[0]+1]
		newPathID = int(random.choice(newPathIDList))

		# set new paths
		cmd = "sudo ./set_path.py -p %d" % (newPathID)
		status, output = commands.getstatusoutput(cmd)
		if status != 0:
			print "Error: cannot set new path"
			return
		print "Set new path successfully! Path:", swid_paths[newPathID], '\n'

		# update current switches
		CURRENT_L2_SW, CURRENT_L3_SW = newl2sw, newl3sw

		# reset counters 
		reset_all_counters()

	elif flag1 == True and flag2 == False:
		for i in l2_overhead:
                        print "Warnning: l2 s%d exceeds the threshold!" % i

		newl2sw_idx = random.randint(0, len(tgtl2sw)-1)
                newl2sw = tgtl2sw[newl2sw_idx]
                newl3sw = CURRENT_L3_SW

                newPath.append(newl2sw)
                newPath.append(newl3sw)

		newPathID, newPathIDList = -1, []
                for item in enumerate(paths):
                        if item[1] == newPath:
                                newPathIDList.append(item[0]+1)
                                print "Find an avaliable path:", swid_paths[item[0]+1]
                newPathID = int(random.choice(newPathIDList))

                # set new paths
                cmd = "sudo ./set_path.py -p %d" % (newPathID)
                status, output = commands.getstatusoutput(cmd)
                if status != 0:
                        print "Error: cannot set new path"
                        return
                print "Set new path successfully! Path:", swid_paths[newPathID], '\n'

		# update current switches
                CURRENT_L2_SW, CURRENT_L3_SW = newl2sw, newl3sw

		# reset counters 
		reset_all_counters()

	elif flag1 == False and flag2 == True:
                for i in l3_overhead:
                        print "Warnning: l3 s%d exceeds the threshold!" % i

                newl2sw = CURRENT_L2_SW
                newl3sw_idx = random.randint(0, len(tgtl3sw)-1)
                newl3sw = tgtl3sw[newl3sw_idx]

                newPath.append(newl2sw)
                newPath.append(newl3sw)

		newPathID, newPathIDList = -1, []
                for item in enumerate(paths):
                        if item[1] == newPath:
                                newPathIDList.append(item[0]+1)
                                print "Find an avaliable path:", swid_paths[item[0]+1]
                newPathID = int(random.choice(newPathIDList))

                # set new paths
                cmd = "sudo ./set_path.py -p %d" % (newPathID)
                status, output = commands.getstatusoutput(cmd)
                if status != 0:
                        print "Error: cannot set new path"
                        return
                print "Set new path successfully! Path:", swid_paths[newPathID], '\n'

                CURRENT_L2_SW, CURRENT_L3_SW = newl2sw, newl3sw

		# reset counters 
		reset_all_counters()

	else:
		reset_all_counters()

if __name__ == '__main__':
    time_interval = args.interval
    try:
        while True: 
		main()
		sleep(time_interval)
    except KeyboardInterrupt:
        print 'User Interrupted'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
