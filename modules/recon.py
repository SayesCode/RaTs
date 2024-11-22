import socket
from ipwhois import IPWhois
from scapy.all import sr1, IP, TCP
from utils.helpers import validate_domain

def dns_lookup(domain):
    if not validate_domain(domain):
        print(f"Invalid domain: {domain}")
        return
    try:
        print(f"Resolving DNS for {domain}...")
        ip = socket.gethostbyname(domain)
        print(f"IP Address: {ip}")
        return ip
    except Exception as e:
        print(f"DNS resolution failed: {e}")

def whois_lookup(ip):
    try:
        print(f"Performing WHOIS lookup for {ip}...")
        obj = IPWhois(ip)
        results = obj.lookup_rdap()
        print(f"WHOIS Data: {results['network']['name']}")
    except Exception as e:
        print(f"WHOIS lookup failed: {e}")

def port_scan(ip):
    print(f"Scanning ports on {ip}...")
    for port in range(20, 1025):
        pkt = sr1(IP(dst=ip)/TCP(dport=port, flags="S"), timeout=0.5, verbose=0)
        if pkt and pkt.haslayer(TCP) and pkt.getlayer(TCP).flags == 0x12:
            print(f"Port {port} is open.")

def perform_recon():
    domain = input("Enter a domain to analyze: ")
    ip = dns_lookup(domain)
    if not ip:
        return

    whois_lookup(ip)

    scan = input("Do you want to scan ports? (y/n): ")
    if scan.lower() == 'y':
        port_scan(ip)
