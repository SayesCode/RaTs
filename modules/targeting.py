from scapy.all import sr1, IP, ICMP
from utils.helpers import validate_ip

def ping_target(ip):
    if not validate_ip(ip):
        print(f"Invalid IP address: {ip}")
        return
    print(f"Pinging {ip}...")
    pkt = sr1(IP(dst=ip)/ICMP(), timeout=1, verbose=0)
    if pkt:
        print(f"{ip} is reachable.")
    else:
        print(f"{ip} is not reachable.")

def traceroute_target(ip):
    if not validate_ip(ip):
        print(f"Invalid IP address: {ip}")
        return
    print(f"Tracing route to {ip}...")
    for ttl in range(1, 30):
        pkt = sr1(IP(dst=ip, ttl=ttl)/ICMP(), timeout=1, verbose=0)
        if pkt and pkt.haslayer(IP):
            print(f"{ttl}: {pkt.getlayer(IP).src}")
            if pkt.getlayer(IP).src == ip:
                break

def perform_targeting():
    ip = input("Enter an IP to target: ")
    ping_target(ip)

    trace = input("Do you want to perform traceroute? (y/n): ")
    if trace.lower() == 'y':
        traceroute_target(ip)
