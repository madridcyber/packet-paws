#!/usr/bin/env python3
"""
port_peek.py — 🔎 a tiny TCP connect scanner

Teaches: sockets, TCP connect scanning, timeouts, basic concurrency.

LEGAL / ETHICAL USE ONLY:
    Scan only hosts you own or have explicit written permission to test.
    Unauthorized port scanning may be illegal in your jurisdiction.

Examples:
    python3 port_peek.py 127.0.0.1
    python3 port_peek.py 127.0.0.1 -p 20-1024
    python3 port_peek.py scanme.nmap.org -p 22,80,443 -t 1.0
"""
import argparse
import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# A few well-known ports so the output is friendlier.
COMMON = {
    21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns",
    80: "http", 110: "pop3", 143: "imap", 443: "https", 445: "smb",
    3306: "mysql", 3389: "rdp", 5432: "postgres", 6379: "redis", 8080: "http-alt",
}


def parse_ports(spec):
    """Turn '20-25,80,443' into a sorted list of ints."""
    ports = set()
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if "-" in chunk:
            lo, hi = chunk.split("-", 1)
            ports.update(range(int(lo), int(hi) + 1))
        elif chunk:
            ports.add(int(chunk))
    return sorted(p for p in ports if 0 < p < 65536)


def peek(host, port, timeout):
    """Return port if a TCP handshake succeeds, else None."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            if s.connect_ex((host, port)) == 0:
                return port
        except OSError:
            pass
    return None


def main():
    ap = argparse.ArgumentParser(description="🐾 packet-paws :: tiny TCP connect scanner")
    ap.add_argument("host", help="target hostname or IP (must be authorized!)")
    ap.add_argument("-p", "--ports", default="1-1024", help="e.g. 22,80,443 or 20-1024")
    ap.add_argument("-t", "--timeout", type=float, default=0.5, help="per-port timeout (s)")
    ap.add_argument("-w", "--workers", type=int, default=100, help="concurrent sockets")
    args = ap.parse_args()

    try:
        ip = socket.gethostbyname(args.host)
    except socket.gaierror:
        print(f"[x] could not resolve host: {args.host}")
        sys.exit(1)

    ports = parse_ports(args.ports)
    print(f"🐈 pouncing on {args.host} ({ip}) — {len(ports)} ports\n")

    open_ports = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(peek, ip, p, args.timeout): p for p in ports}
        for fut in as_completed(futures):
            port = fut.result()
            if port:
                name = COMMON.get(port, "?")
                print(f"  [+] {port:>5}/tcp  open   {name}")
                open_ports.append(port)

    print(f"\n🐾 done. {len(open_ports)} open port(s): {sorted(open_ports)}")


if __name__ == "__main__":
    main()
