#!/usr/bin/env python3
"""
Automated Nmap Network Scanner
Wraps Nmap in a Python CLI for structured reconnaissance output.

Author: Sagar Bidari
Monash University Cybersecurity Bootcamp

Usage:
    python scanner.py --target 192.168.1.0/24
    python scanner.py --target 192.168.1.100 --mode full --output results.json
    python scanner.py --target 192.168.1.0/24 --mode quick --output results.csv

Requires nmap installed on the host (`sudo apt install nmap`) and the
`python-nmap` package (`pip install python-nmap`).
"""

import argparse
import csv
import json
import sys
from datetime import datetime, timezone

try:
    import nmap
except ImportError:
    print("Missing dependency: pip install python-nmap", file=sys.stderr)
    sys.exit(1)

SCAN_PROFILES = {
    "quick": "-T4 -F",
    "full": "-sV -T4 -p-",
    "service": "-sV -T4",
    "os": "-O -T4",
}


def run_scan(target: str, mode: str) -> dict:
    """Run an Nmap scan against `target` using the named profile and return
    a structured dict of host -> scan results."""
    scanner = nmap.PortScanner()
    args = SCAN_PROFILES.get(mode, SCAN_PROFILES["quick"])

    scanner.scan(hosts=target, arguments=args)

    results = {
        "target": target,
        "mode": mode,
        "nmap_args": args,
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "hosts": [],
    }

    for host in scanner.all_hosts():
        host_info = {
            "host": host,
            "status": scanner[host].state(),
            "ports": [],
            "os_guess": None,
        }

        if "osmatch" in scanner[host] and scanner[host]["osmatch"]:
            host_info["os_guess"] = scanner[host]["osmatch"][0].get("name")

        for proto in scanner[host].all_protocols():
            for port in sorted(scanner[host][proto].keys()):
                port_data = scanner[host][proto][port]
                host_info["ports"].append(
                    {
                        "port": port,
                        "protocol": proto,
                        "state": port_data.get("state"),
                        "service": port_data.get("name"),
                        "version": (
                            f"{port_data.get('product', '')} {port_data.get('version', '')}".strip()
                            or None
                        ),
                    }
                )

        results["hosts"].append(host_info)

    return results


def write_json(results: dict, path: str) -> None:
    with open(path, "w") as f:
        json.dump(results, f, indent=2)


def write_csv(results: dict, path: str) -> None:
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["host", "status", "os_guess", "port", "protocol", "state", "service", "version"])
        for host in results["hosts"]:
            if not host["ports"]:
                writer.writerow([host["host"], host["status"], host["os_guess"], "", "", "", "", ""])
                continue
            for p in host["ports"]:
                writer.writerow(
                    [
                        host["host"],
                        host["status"],
                        host["os_guess"],
                        p["port"],
                        p["protocol"],
                        p["state"],
                        p["service"],
                        p["version"],
                    ]
                )


def main():
    parser = argparse.ArgumentParser(
        description="Automate Nmap network reconnaissance and export structured results."
    )
    parser.add_argument("--target", required=True, help="IP, CIDR range, or hostname to scan")
    parser.add_argument(
        "--mode",
        choices=SCAN_PROFILES.keys(),
        default="quick",
        help="Scan profile: quick | full | service | os (default: quick)",
    )
    parser.add_argument("--output", help="Path to write results (.json or .csv). Omit to print to stdout.")
    args = parser.parse_args()

    print(f"[*] Scanning {args.target} (mode={args.mode})... this may take a while.")
    results = run_scan(args.target, args.mode)

    if not args.output:
        print(json.dumps(results, indent=2))
        return

    if args.output.endswith(".csv"):
        write_csv(results, args.output)
    else:
        write_json(results, args.output)

    print(f"[+] {len(results['hosts'])} host(s) scanned. Results written to {args.output}")


if __name__ == "__main__":
    main()
