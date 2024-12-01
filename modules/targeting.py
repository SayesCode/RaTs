from scapy.all import sr1, IP, ICMP
from utils.helpers import validate_ip

def ping_target(ip):
    """
    Send an ICMP ping to the target IP and report if it is reachable.
    """
    if not validate_ip(ip):
        print(f"Error: '{ip}' is not a valid IP address.")
        return

    print(f"Pinging {ip}...")
    response = sr1(IP(dst=ip) / ICMP(), timeout=1, verbose=0)
    if response:
        print(f"Success: {ip} is reachable.")
    else:
        print(f"Failure: {ip} is not reachable.")

def traceroute_target(ip, max_hops=30):
    """
    Perform a traceroute to the target IP, printing each hop.
    """
    if not validate_ip(ip):
        print(f"Error: '{ip}' is not a valid IP address.")
        return

    print(f"Tracing route to {ip} with a maximum of {max_hops} hops...")
    for ttl in range(1, max_hops + 1):
        response = sr1(IP(dst=ip, ttl=ttl) / ICMP(), timeout=1, verbose=0)
        if response and response.haslayer(IP):
            src_ip = response.getlayer(IP).src
            print(f"{ttl}: {src_ip}")
            if src_ip == ip:
                print(f"Traceroute complete: {ip} reached in {ttl} hops.")
                break
        else:
            print(f"{ttl}: Request timed out.")
    else:
        print(f"Traceroute incomplete: Maximum hops ({max_hops}) reached.")

def perform_targeting():
    """
    Handle user input to perform a ping and optional traceroute on a target IP.
    """
    ip = input("Enter an IP address to target: ").strip()

    # Perform ping
    ping_target(ip)

    # Ask for traceroute
    trace_option = input("Do you want to perform a traceroute? (y/n): ").strip().lower()
    if trace_option == 'y':
        traceroute_target(ip)
