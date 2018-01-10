#!/usr/bin/env python

import struct
import sys
import argparse
import commands
from time import sleep

_THRIFT_BASE_PORT = 22222

# Switch IDs of specific path
paths = [[1,2,3],[1,2,3],[1,2,4],[1,2,4],[1,5,3],[1,5,3],[1,5,4],[1,5,4]]

parser = argparse.ArgumentParser(description='SDN & P4 Demo')
parser.add_argument('-p', '--path', help='Path ID',
                    type=int, action="store", default=1)
args = parser.parse_args()

def main():
	# Path => Switch ID => Thrift Port
	pathID = args.path
	swIDList = paths[pathID-1]
	thriftPortList = []
	for swid in swIDList:
		thriftPortList.append(swid+_THRIFT_BASE_PORT-1)

	# Cleanup original rules
        cmd = "sudo ./reset_all_switches.sh"
        status, output = commands.getstatusoutput(cmd)
	print output
        if status != 0:
                print "\nError: switch cannot be reset!\n"
		return


	# Populate runtime rules
	for i in range(len(thriftPortList)):
		# No.i+1 layer
		layerID = i+1
		layerRule = "l%d.txt" % layerID
		# thrift port
		thriftPort = thriftPortList[i]

		# set_path.sh: 
		# sudo ./simple_switch_CLI --thrift-port $1 < rules/path$2/$3
		cmd = "sudo ./set_path.sh %d %d %s" % (thriftPortList[i], pathID, layerRule)
		status, output = commands.getstatusoutput(cmd)
		print output
		if status != 0:
			print "\nError: cannot set path in switch%d!\n" % (thriftPort-_THRIFT_BASE_PORT+1)
			return

if __name__ == '__main__':
	main()

