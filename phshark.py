import sys
from scapy.all import *

# 패킷 캡쳐?
while True :
    sniff(iface="Wi-Fi", prn = lambda x:x.show())