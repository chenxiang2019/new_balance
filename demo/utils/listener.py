#!/usr/bin/env python
import sys
import struct
import argparse
import commands

from scapy.all import sniff, sendp, hexdump, get_if_list, get_if_hwaddr
from scapy.all import Packet, IPOption
from scapy.all import IP, TCP, ICMP, UDP, Raw 

parser = argparse.ArgumentParser(description='Listener')
parser.add_argument('-p', '--port', help='listen port', 
                    type=str, action="store", default='non')
parser.add_argument('-s', '--switch-name', help='switch name',
                    type=str, action="store", default='s1')
args = parser.parse_args()

_THRIFT_BASE_PORT = 22222

counter = 0

# listen port
server1, server2, server3, server4 = 0,0,0,0

def handle_tcp_pkt(packet, thrift_port):
    global counter
    counter = counter+1
    return 'TCP Packet #{}: {} ==> {}, sport {} ==> dport {}'.format(counter, packet[0][1].src, packet[0][1].dst, packet[TCP].sport, packet[TCP].dport)

def handle_udp_pkt(packet, thrift_port):
    global counter
    counter = counter+1
    return 'UDP Packet #{}: {} ==> {}, sport {} ==> dport {}'.format(counter, packet[0][1].src, packet[0][1].dst, packet[UDP].sport, packet[UDP].dport)

def report(sniff_on):
    global server1, server2, server3, server4
    if sniff_on == "s3-eth3":
        server1 += 1
    elif sniff_on == "s3-eth4":
        server2 += 1
    elif sniff_on == "s4-eth3":
        server3 += 1
    elif sniff_on == "s4-eth4":
        server4 += 1
    else:
        print "You are not listen to the default port lists."
        print "Get a packet at %s" % sniff_on
        return

    print "\n============================================================"
    print "s3-eth3: %d, s3-eth4: %d, s4-eth3: %d, s4-eth4: %d" % (server1, server2, server3, server4)
    print "============================================================\n"
        

def main():
    # Get Thrift Port
    sw_name = args.switch_name
    index = int(sw_name[1:])-1
    thrift_port = _THRIFT_BASE_PORT+index

    iface = args.port
    if iface == "non":
        iface = ["s3-eth3", "s3-eth4", "s4-eth3", "s4-eth4"]

    print "sniffing on %s" % iface
    sys.stdout.flush()
    # sniff(filter="udp", iface = iface, prn = lambda x: handle_udp_pkt(x, thrift_port))
    sniff(filter="udp and port 340", iface=iface, prn=lambda x: report(x.sniffed_on))

if __name__ == '__main__':
    main()

