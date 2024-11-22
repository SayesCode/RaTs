import re

def validate_domain(domain):
    """Validate if the domain is in a valid format."""
    pattern = r"^(?:[a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,6}$"
    return re.match(pattern, domain)

def validate_ip(ip):
    """Validate if the IP address is in a valid format."""
    pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"
    return re.match(pattern, ip)
