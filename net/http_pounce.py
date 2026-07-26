#!/usr/bin/env python3
"""
http_pounce.py — 📡 fetch a URL and audit its security headers

Teaches: HTTP requests with the stdlib, response headers, and what the
common security headers do. A friendly first look at a web target.

Use only on sites you own or are authorized to assess.

Examples:
    python3 http_pounce.py https://example.com
    python3 http_pounce.py http://localhost:8080
"""
import argparse
import ssl
import urllib.request
import urllib.error

# header -> why you care
SECURITY_HEADERS = {
    "Strict-Transport-Security": "forces HTTPS (HSTS)",
    "Content-Security-Policy": "mitigates XSS / injection",
    "X-Frame-Options": "clickjacking protection",
    "X-Content-Type-Options": "stops MIME sniffing",
    "Referrer-Policy": "controls referrer leakage",
    "Permissions-Policy": "limits browser features",
}


def fetch(url, timeout):
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "packet-paws/1.0 (+labs)"})
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        return resp.status, dict(resp.headers)


def main():
    ap = argparse.ArgumentParser(description="🐾 packet-paws :: HTTP header pounce")
    ap.add_argument("url", help="target URL (http:// or https://)")
    ap.add_argument("-t", "--timeout", type=float, default=8.0, help="request timeout (s)")
    args = ap.parse_args()

    try:
        status, headers = fetch(args.url, args.timeout)
    except urllib.error.HTTPError as e:
        status, headers = e.code, dict(e.headers)
    except Exception as e:  # noqa: BLE001 — keep the demo forgiving
        print(f"[x] request failed: {e}")
        return

    print(f"📡 {args.url} — HTTP {status}\n")

    server = headers.get("Server")
    powered = headers.get("X-Powered-By")
    if server:
        print(f"  🐾 Server: {server}")
    if powered:
        print(f"  🐾 X-Powered-By: {powered}  (consider hiding this)")

    print("\n🔐 security header audit:")
    present = 0
    for name, why in SECURITY_HEADERS.items():
        if name in headers:
            present += 1
            print(f"  [✓] {name:<28} {why}")
        else:
            print(f"  [ ] {name:<28} MISSING — {why}")

    score = present * 100 // len(SECURITY_HEADERS)
    print(f"\n🏆 hardening score: {present}/{len(SECURITY_HEADERS)} ({score}%)")


if __name__ == "__main__":
    main()
