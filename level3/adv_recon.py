
import argparse
import json
import subprocess
import requests
import os
import whois
import dns.resolver
from jinja2 import Environment, FileSystemLoader


GOWITNESS_PATH = "C:\\Users\\Krish Sharma\\go\\bin\\gowitness.exe"
SHODAN_API_KEY = "ACi34MQlWckleLUSu4rz8dOtxQtrnVoJ"

def get_subdomains(domain):
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        response = requests.get(url, timeout=10)
        data = response.json()
        subdomains = sorted(set(entry['name_value'] for entry in data))
        return subdomains
    except Exception as e:
        return [f"Error retrieving subdomains: {e}"]

def get_dns_records(domain):
    record_types = ["A", "NS", "MX"]
    dns_records = {}
    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            dns_records[rtype] = [str(r.to_text()) for r in answers]
        except Exception:
            dns_records[rtype] = []
    return dns_records

def get_whois(domain):
    try:
        w = whois.whois(domain)
        return json.dumps(w, indent=2, default=str)
    except Exception as e:
        return f"WHOIS failed: {e}"

def get_http_headers(domain):
    try:
        response = requests.get(f"http://{domain}", timeout=10)
        return dict(response.headers)
    except Exception as e:
        return {"Error": str(e)}

def check_robots_sitemap(domain):
    results = {}
    for path in ["robots.txt", "sitemap.xml"]:
        try:
            url = f"http://{domain}/{path}"
            response = requests.get(url, timeout=5)
            results[path] = response.text if response.status_code == 200 else "Not Found"
        except:
            results[path] = "Error"
    return results

def run_nmap(domain):
    try:
        output = subprocess.check_output(
            ["nmap", "--unprivileged", "-sT", "-T4", domain],
            stderr=subprocess.STDOUT,
            timeout=60
        ).decode()
        return output
    except subprocess.CalledProcessError as e:
        return f"Port scan failed: {e.output.decode()}"
    except Exception as e:
        return f"Port scan failed: {e}"


def detect_technologies(domain):
    try:
        output = subprocess.check_output(["whatweb", domain], timeout=30).decode()
        return output
    except Exception as e:
        return f"Tech detection failed: {e}"

def extract_emails(domain):
    try:
        output = subprocess.check_output([
            "theHarvester", "-d", domain, "-b", "duckduckgo,baidu"
        ], timeout=60).decode()
        emails = [line for line in output.splitlines() if "@" in line]
        return emails
    except Exception as e:
        return [f"Email harvesting failed: {e}"]

def shodan_lookup(domain):
    try:
        ip = requests.get(f"https://dns.google/resolve?name={domain}&type=A").json()["Answer"][0]["data"]
        response = requests.get(f"https://api.shodan.io/shodan/host/{ip}?key={SHODAN_API_KEY}", timeout=10)
        return response.json()
    except Exception as e:
        return f"Shodan lookup failed: {e}"

def run_wafw00f(domain):
    try:
        output = subprocess.check_output(["wafw00f", domain], timeout=30).decode()
        return output
    except Exception as e:
        return f"WAF detection failed: {e}"

def take_screenshots(domain):
    try:
        with open("targets.txt", "w") as f:
            f.write(f"https://{domain}\nhttp://{domain}")
        subprocess.run([GOWITNESS_PATH, "scan", "file", "-f", "targets.txt", "--screenshot-path", "./screenshots"], check=True)
        return "Screenshots captured."
    except Exception as e:
        return f"Screenshot capture failed: {e}"

def generate_html_report(domain, data):
    env = Environment(loader=FileSystemLoader(searchpath="./templates"))
    template = env.get_template("report.html")
    output = template.render(domain=domain, data=data)
    with open(f"{domain}_report.html", "w", encoding="utf-8") as f:
        f.write(output)
    print(f"[+] HTML report saved to {domain}_report.html")

def main():
    parser = argparse.ArgumentParser(description="Advanced Recon Tool")
    parser.add_argument("domain", help="Target domain to scan")
    parser.add_argument("-o", "--output", help="Output report filename")
    args = parser.parse_args()

    domain = args.domain
    report = {
        "subdomains": get_subdomains(domain),
        "dns": get_dns_records(domain),
        "whois": get_whois(domain),
        "headers": get_http_headers(domain),
        "robots_sitemap": check_robots_sitemap(domain),
        "port_scan": run_nmap(domain),
        "technologies": detect_technologies(domain),
        "emails": extract_emails(domain),
        "shodan": shodan_lookup(domain),
        "waf": run_wafw00f(domain),
        "screenshots": take_screenshots(domain)
    }

    generate_html_report(domain, report)

def run_recon(domain, modules):
    report = {}

    if modules.get("subdomains"):
        report["subdomains"] = get_subdomains(domain)
    if modules.get("dns"):
        report["dns"] = get_dns_records(domain)
    if modules.get("whois"):
        report["whois"] = get_whois(domain)
    if modules.get("headers"):
        report["headers"] = get_http_headers(domain)
    if modules.get("robots_sitemap"):
        report["robots_sitemap"] = check_robots_sitemap(domain)
    if modules.get("port_scan"):
        report["port_scan"] = run_nmap(domain)
    if modules.get("technologies"):
        report["technologies"] = detect_technologies(domain)
    if modules.get("emails"):
        report["emails"] = extract_emails(domain)
    if modules.get("shodan"):
        report["shodan"] = shodan_lookup(domain)
    if modules.get("waf"):
        report["waf"] = run_wafw00f(domain)
    if modules.get("screenshots"):
        report["screenshots"] = take_screenshots(domain)

    generate_html_report(domain, report)
    return report
