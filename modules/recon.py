import socket
from ipwhois import IPWhois
from scapy.all import sr1, IP, TCP
import whois
import re
import requests
import ssl
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

# Chaves de API do arquivo .env
NUMVERIFY_API_KEY = os.getenv("NUMVERIFY_API_KEY")
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")

# Função para validar e sanitizar o domínio
def validate_domain(domain):
    pattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, domain))

# Resolução DNS
def dns_lookup(domain):
    if not validate_domain(domain):
        print(f"Invalid domain: {domain}")
        return None
    try:
        print(f"Resolving DNS for {domain}...")
        ip = socket.gethostbyname(domain)
        print(f"IP Address: {ip}")
        return ip
    except Exception as e:
        print(f"DNS resolution failed: {e}")
        return None

# Consulta WHOIS para IP
def whois_ip_lookup(ip):
    try:
        print(f"Performing WHOIS lookup for IP {ip}...")
        obj = IPWhois(ip)
        results = obj.lookup_rdap()
        print("WHOIS IP Data:")
        for key, value in results['network'].items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"WHOIS lookup for IP failed: {e}")

# Consulta WHOIS para domínio
def whois_domain_lookup(domain):
    try:
        print(f"\nPerforming WHOIS lookup for domain {domain}...\n")
        w = whois.whois(domain)
        print("WHOIS Domain Data:")
        
        # Organizar e imprimir os dados do WHOIS
        for key, value in w.items():
            print(f"  {key.capitalize()}: {value}")

        # Verificar presença de CNPJ no campo 'Registrant_id'
        registrant_id = w.get('Registrant_id')
        if registrant_id:
            match_cnpj = re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', registrant_id)
            if match_cnpj:
                cnpj = match_cnpj.group()
                print(f"\nFound CNPJ: {cnpj}")
                fetch_cnpj_data(cnpj)

        # Verificar presença de e-mails
        if 'email' in w:  # Verifica se o campo 'email' existe
            email = w['email']
            if isinstance(email, list):  # Quando for uma lista de e-mails
                for e in email:
                    print(f"Found Email: {e}")
                    fetch_email_data(e)
            elif isinstance(email, str):  # Quando for um único e-mail
                print(f"Found Email: {email}")
                fetch_email_data(email)

        # Verificar presença de telefone
        if 'phone' in w:  # Verifica se o campo 'phone' existe
            print(f"Found Phone: {w['phone']}")
            fetch_phone_data(w['phone'])

    except Exception as e:
        print(f"WHOIS lookup for domain failed: {e}")




# Busca dados de CNPJ usando a API ReceitaWS
def fetch_cnpj_data(cnpj):
    url = f"https://receitaws.com.br/v1/cnpj/{cnpj}"
    try:
        print(f"\nFetching additional data for CNPJ {cnpj}...")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("CNPJ Data:")
            print(f"  Nome: {data.get('nome')}")
            print(f"  Atividade Principal: {data.get('atividade_principal', [{}])[0].get('text')}")
            print(f"  UF: {data.get('uf')}")
            print(f"  Status: {data.get('situacao')}")

            # Extração de telefone e e-mail do CNPJ
            if data.get('telefone'):
                print(f"Phone: {data['telefone']}")
                fetch_phone_data(data['telefone'])
            if data.get('email'):
                print(f"Email: {data['email']}")
                fetch_email_data(data['email'])
        else:
            print(f"Failed to fetch CNPJ data: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error fetching CNPJ data: {e}")

# Busca dados de telefone usando NumVerify API
def fetch_phone_data(phone):
    if not NUMVERIFY_API_KEY:
        print("NumVerify API key not found in .env")
        return
    url = f"https://api.apilayer.com/number_verification/validate?access_key={NUMVERIFY_API_KEY}&number={phone}"
    try:
        print(f"\nFetching additional data for Phone: {phone}...")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("Phone Data:")
            print(f"  Country: {data.get('country_name')}")
            print(f"  Valid: {data.get('valid')}")
            print(f"  Carrier: {data.get('carrier')}")
        else:
            print(f"Failed to fetch phone data: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error fetching phone data: {e}")

# Busca dados de e-mail usando API Hunter.io
def fetch_email_data(email):
    if not HUNTER_API_KEY:
        print("Hunter.io API key not found in .env")
        return
    url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={HUNTER_API_KEY}"
    try:
        print(f"\nFetching additional data for Email: {email}...")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("Email Data:")
            print(f"  Valid: {data['data']['result']}")
            print(f"  Score: {data['data']['score']}")
        else:
            print(f"Failed to fetch email data: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error fetching email data: {e}")

# Verificação de certificado SSL
def ssl_certificate_check(domain):
    try:
        print(f"\nChecking SSL certificate for {domain}...\n")
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                print("SSL Certificate:")
                for key, value in cert.items():
                    print(f"  {key}: {value}")
    except Exception as e:
        print(f"SSL check failed: {e}")

def port_scan(ip):
    print(f"Scanning ports on {ip}...")
    open_ports = []
    for port in range(20, 1025):  # Escaneia portas comuns de 20 a 1024
        pkt = sr1(IP(dst=ip)/TCP(dport=port, flags="S"), timeout=0.5, verbose=0)
        if pkt and pkt.haslayer(TCP) and pkt.getlayer(TCP).flags == 0x12:
            open_ports.append(port)
            print(f"Port {port} is open.")
    if not open_ports:
        print("No open ports found.")

# Função principal
def perform_recon():
    domain = input("Enter a domain to analyze: ")
    ip = dns_lookup(domain)
    if not ip:
        return

    print("\n--- WHOIS Lookup ---")
    whois_domain_lookup(domain)
    whois_ip_lookup(ip)

    ssl_check = input("\nDo you want to check SSL certificate? (y/n): ")
    if ssl_check.lower() == 'y':
        ssl_certificate_check(domain)

    scan = input("\nDo you want to scan ports? (y/n): ")
    if scan.lower() == 'y':
        print("\n--- Port Scan ---")
        port_scan(ip)

# Chamada do programa
if __name__ == "__main__":
    perform_recon()
