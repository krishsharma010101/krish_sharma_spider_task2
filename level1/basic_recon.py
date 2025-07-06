import os
import sys
import requests
import socket
import json
import whois
import subprocess
import dns.resolver

def get_domain():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return input("Enter a domain: ").strip()

def enumerate_subdomains(domain):
    print("\nEnumerating Subdomains using crt.sh...")
    try:
        response = requests.get(f"https://crt.sh/?q=%25.{domain}&output=json", timeout=10)
        subdomains = set()
        for entry in response.json():
            name = entry['name_value']
            for sub in name.split('\n'):
                if domain in sub:
                    subdomains.add(sub.strip())
        return sorted(subdomains)
    except Exception as e:
        print(f"Error fetching from crt.sh: {e}")
        return []

def lookup_dns_records(domain):
    print("\nPerforming DNS Record Lookup...")
    records = {}
    try:
        for record_type in ['A', 'NS', 'MX']:
            answers = dns.resolver.resolve(domain, record_type)
            records[record_type] = [str(r.to_text()) for r in answers]
    except Exception as e:
        print(f"DNS error: {e}")
    return records

def get_whois(domain):
    print("\nPerforming WHOIS Lookup...")
    try:
        return str(whois.whois(domain))
    except:
        print("Falling back to CLI 'whois' command...")
        return subprocess.getoutput(f"whois {domain}")

def get_http_headers(domain):
    print("\nFetching HTTP Headers...")
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        return response.headers
    except Exception as e:
        return {"Error": str(e)}

def fetch_robots_sitemap(domain):
    print("\nRetrieving robots.txt and sitemap.xml...")
    data = {}
    for path in ['robots.txt', 'sitemap.xml']:
        url = f"http://{domain}/{path}"
        try:
            r = requests.get(url, timeout=5)
            data[path] = r.text if r.status_code == 200 else f"Not found (HTTP {r.status_code})"
        except Exception as e:
            data[path] = f"Error: {e}"
    return data

def geoip_lookup(domain):
    print("\nPerforming GeoIP Lookup...")
    try:
        ip = socket.gethostbyname(domain)
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        return r.json()
    except Exception as e:
        return {"Error": str(e)}

def save_output(domain, data):
    filename = f"basic_{domain.replace('.', '_')}.txt"
    with open(filename, 'w') as f:
        f.write(data)
    print(f"\nOutput saved to: {filename}")

def main():
    domain = get_domain()
    results = []

    # Subdomains
    subdomains = enumerate_subdomains(domain)
    results.append(f"\nSubdomains:\n" + "\n".join(subdomains) if subdomains else "No subdomains found")

    # DNS Records
    dns_records = lookup_dns_records(domain)
    for record_type, values in dns_records.items():
        results.append(f"\n{record_type} Records:\n" + "\n".join(values))

    # WHOIS
    results.append(f"\nWHOIS Info:\n{get_whois(domain)}")

    # HTTP Headers
    headers = get_http_headers(domain)
    results.append("\nHTTP Headers:")
    results.extend([f"{k}: {v}" for k, v in headers.items()])

    # robots.txt & sitemap.xml
    bot_files = fetch_robots_sitemap(domain)
    for name, content in bot_files.items():
        results.append(f"\n{name}:\n{content}")

    # GeoIP
    geo = geoip_lookup(domain)
    results.append("\nGeoIP Info:")
    results.extend([f"{k}: {v}" for k, v in geo.items()])

    # Output
    full_output = "\n".join(results)
    print(full_output)
    save_output(domain, full_output)

if __name__ == "__main__":
    main()
