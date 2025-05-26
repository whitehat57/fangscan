#!/usr/bin/env python3
import argparse
import json
import socket
import urllib3

from core.ssl_info import get_ssl_info
from core.tech_detect import detect_cms, detect_js_frameworks, builtwith_tech
from core.cdn_check import check_cdn
from core.dns_enum import get_dns_records
from core.headers import get_headers, check_security_headers
from utils.printer import print_colored, init_color
from colorama import Fore, Style

# Disable SSL/TLS warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def print_banner():
    banner = f"""{Fore.CYAN}{Style.BRIGHT}
88P'888'Y88                  888             d8                    888   
P'  888  'Y  ,e e,   e88'888 888 ee   dP"Y  d88    ,"Y88b  e88'888 888 ee
    888     d88 88b d888  '8 888 88b C88b  d88888 "8" 888 d888  '8 888 P 
    888     888   , Y888   , 888 888  Y88D  888   ,ee 888 Y888   , 888 b 
    888      "YeeP"  "88,e8' 888 888 d,dP   888   "88 888  "88,e8' 888 8b v2.0
{Fore.YELLOW}                      FangScan - Web Recon by Harpy 🦅
"""
    print(banner)

def pretty_print_results(result, no_color=False):
    def section(title):
        print_colored(f"\n[+] {title}:", "cyan", no_color)

    def bullet(label, value=None, indent=2):
        prefix = " " * indent + "├─ "
        val = f"{value}" if value else label
        print_colored(prefix + val, "white", no_color)

    url = result.get("url", "Unknown")
    hostname = url.split("//")[-1].split("/")[0]
    ip = socket.gethostbyname(hostname) if hostname else "Unknown"

    print_colored(f"\nURL: {url}", "green", no_color)
    print_colored(f"IP : {ip}", "green", no_color)

    if "technologies" in result:
        section("Teknologi yang Terdeteksi")
        for category, items in result["technologies"].items():
            print_colored(f"\n{category.lower()}:", "yellow", no_color)
            for tech in items:
                bullet(tech)

    if "javascript_frameworks" in result:
        section("JavaScript Frameworks")
        for js in result["javascript_frameworks"]:
            bullet(js)

    if "cms" in result:
        section("CMS Terdeteksi")
        for cms, reason in result["cms"].items():
            bullet(f"{cms} ({reason})")

    if "server_info" in result:
        section("Informasi Server")
        srv = result["server_info"]
        bullet("Server", srv.get("server", "Unknown"))
        bullet("Powered By", srv.get("x_powered_by", "Unknown"))
        bullet("HTTP/3 Support", "Yes" if srv.get("http3_support") else "No")
        bullet("CDN", srv.get("cdn", "Unknown"))

    if "domain_info" in result:
        section("Informasi Domain")
        dom = result["domain_info"]
        bullet("Registrar", dom.get("registrar", "Unknown"))
        bullet("Tanggal Pembuatan", dom.get("creation_date", "Unknown"))
        bullet("Tanggal Kadaluarsa", dom.get("expiration_date", "Unknown"))

    if "ssl_info" in result:
        section("Informasi SSL")
        ssl = result["ssl_info"]
        bullet("Issuer", ssl.get("issuer", "Unknown"))
        bullet("Valid From", ssl.get("valid_from", "Unknown"))
        bullet("Valid Until", ssl.get("valid_until", "Unknown"))
        bullet("TLS Version", ssl.get("tls_version", "Unknown"))

    if "headers" in result:
        section("Security Headers")
        for h, v in result["headers"].items():
            if isinstance(v, dict):
                bullet(h, v.get("status"))
            else:
                bullet(h, v)

    if "dns" in result:
        section("DNS Records")
        for rtype, records in result["dns"].items():
            print_colored(f"\n{rtype}:", "yellow", no_color)
            for record in records:
                bullet(record)

def main():
    init_color()
    print_banner()

    parser = argparse.ArgumentParser(description="🦅 FangScan - Web Recon Toolkit by Harpy")
    parser.add_argument("-u", "--url", required=True, help="Target URL (with or without https://)")
    parser.add_argument("--cms", action="store_true", help="Detect CMS only")
    parser.add_argument("--headers", action="store_true", help="Check security headers")
    parser.add_argument("--ssl", action="store_true", help="Grab SSL certificate info")
    parser.add_argument("--cdn", action="store_true", help="Detect CDN provider")
    parser.add_argument("--dns", action="store_true", help="Enumerate DNS records")
    parser.add_argument("--all", action="store_true", help="Run full scan")
    parser.add_argument("--save", metavar="FILE", help="Save output as JSON")
    parser.add_argument("--no-color", action="store_true", help="Disable color output")
    args = parser.parse_args()

    url = args.url if args.url.startswith("http") else "https://" + args.url
    hostname = url.split("//")[-1].split("/")[0]
    result = {"url": url}

    print_colored(f"[*] Starting scan on: {url}", "yellow", args.no_color)

    if args.all or args.ssl:
        result["ssl_info"] = get_ssl_info(hostname)

    if args.all or args.cms:
        techs = builtwith_tech(url)
        result["technologies"] = techs
        result["cms"] = detect_cms(url, techs)
        result["javascript_frameworks"] = detect_js_frameworks(url)

    if args.all or args.cdn:
        headers = get_headers(url)
        result["server_info"] = {
            "server": headers.get("Server", "Unknown"),
            "x_powered_by": headers.get("X-Powered-By", "Unknown"),
            "http3_support": "alt-svc" in headers,
            "cdn": check_cdn(headers, hostname).get("detected", "Unknown")
        }

    if args.all or args.dns:
        result["dns"] = get_dns_records(hostname)

    if args.all or args.headers:
        headers = get_headers(url)
        result["headers"] = check_security_headers(headers)

    if args.save:
        with open(args.save, 'w') as f:
            json.dump(result, f, indent=4)
        print_colored(f"[✓] Output saved to {args.save}", "green", args.no_color)

    pretty_print_results(result, args.no_color)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n[!] Scan aborted by user.", "red")
