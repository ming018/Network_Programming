import sys
from scapy.all import *

print(conf.ifaces)

# 패킷 캡쳐?
while True :
    sniff(iface="Software Loopback Interface 1", prn = lambda x:x.show())