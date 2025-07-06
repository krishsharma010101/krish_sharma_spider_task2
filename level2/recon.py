import argparse
import os
import json
import csv
import socket
import subprocess
import requests
import nmap
import shodan

def get_args():
    parser = argparse.ArgumentParser(description="Advanced Recon Tool")
    parser.add_argument("--domain", required=True, help="Target domain (e.g., example.com)")
    parser.add_argument("--scan", action="store_true", help="Enable port scanning and banner grabbing")
    parser.add_argument("--tech", action="store_true", help="Enable technology detection (WhatWeb)")
    parser.add_argument("--emails", action="store_true", help="Enable email harvesting (theHarvester)")
    parser.add_argument("--shodan", action="store_true", help="Enable Shodan lookup (requires SHODAN_API_KEY)")
    parser.add_argument("--report", choices=["json", "csv"], help="Save report in JSON or CSV format")
    return parser.parse_args()

def scan_ports(domain):
    print("\n[+] Scanning ports with Nmap (Unprivileged)...")
    scanner = nmap.PortScanner()
    results = {}
    try:
        scanner.scan(domain, arguments="-Pn -T4 -sT -p 1-1000 --script=banner")
        for proto in scanner[domain].all_protocols():
            results[proto] = {}
            for port in scanner[domain][proto]:
                banner = scanner[domain][proto][port].get('script', {}).get('banner', 'No banner')
                results[proto][port] = banner
    except Exception as e:
        results["error"] = str(e)
    return results

def detect_tech(domain):
    print("\n[+] Detecting web technologies with WhatWeb...")
    try:
        result = subprocess.check_output(
            ["ruby", "C:\\Users\\Krish Sharma\\WhatWeb\\WhatWeb", domain],
            stderr=subprocess.DEVNULL,
            text=True
        )
        return result.strip()
    except Exception as e:
        return str(e)

def harvest_emails(domain):
    print("\n[+] Harvesting emails with theHarvester...")
    try:
        result = subprocess.check_output([
            "theHarvester", "-d", domain, "-b", "baidu,duckduckgo,crtsh", "-l", "100"
        ], text=True)
        return result.strip()
    except Exception as e:
        return str(e)

def shodan_lookup(domain):
    print("\n[+] Querying Shodan...")
    try:
        ip = socket.gethostbyname(domain)
        api_key = os.getenv("SHODAN_API_KEY")
        if not api_key:
            return "Set SHODAN_API_KEY as an environment variable."
        api = shodan.Shodan(api_key)
        host = api.host(ip)
        return host
    except Exception as e:
        return str(e)

def save_report(domain, data, format):
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/{domain.replace('.', '_')}.{format}"
    if format == "json":
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
    elif format == "csv":
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            for key, val in data.items():
                writer.writerow([key, json.dumps(val) if isinstance(val, (dict, list)) else val])
    print(f"\n[+] Report saved to: {filename}")

def main():
    args = get_args()
    domain = args.domain
    report = {}

    if args.scan:
        report["PortScan"] = scan_ports(domain)

    if args.tech:
        report["TechDetection"] = detect_tech(domain)

    if args.emails:
        report["EmailHarvesting"] = harvest_emails(domain)

    if args.shodan:
        report["ShodanLookup"] = shodan_lookup(domain)

    if args.report:
        save_report(domain, report, args.report)
    else:
        print("\n[+] Scan Results:")
        print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
