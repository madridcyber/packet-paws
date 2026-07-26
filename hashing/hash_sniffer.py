#!/usr/bin/env python3
"""
hash_sniffer.py — 🧬 guess a hash's type by its shape

Teaches: how hashes differ by length & alphabet, regex, and why you can
never be 100% sure from shape alone (many algorithms share a length).

This does NOT crack anything — it only classifies. Great for the first 5
seconds of a crypto/forensics challenge.

Examples:
    python3 hash_sniffer.py 5d41402abc4b2a76b9719d911017c592
    python3 hash_sniffer.py $2y$10$N9qo8uLOickgx2ZMRZoM1e...
"""
import argparse
import re

# (name, compiled regex, note). Order matters: most specific first.
SIGNATURES = [
    ("bcrypt",       re.compile(r"^\$2[aby]\$\d{2}\$[./A-Za-z0-9]{53}$"), "password hash, has salt+cost"),
    ("MD5",          re.compile(r"^[a-f0-9]{32}$", re.I), "128-bit — fast, broken, everywhere"),
    ("SHA-1",        re.compile(r"^[a-f0-9]{40}$", re.I), "160-bit — deprecated"),
    ("SHA-224",      re.compile(r"^[a-f0-9]{56}$", re.I), "224-bit"),
    ("SHA-256",      re.compile(r"^[a-f0-9]{64}$", re.I), "256-bit — the workhorse"),
    ("SHA-384",      re.compile(r"^[a-f0-9]{96}$", re.I), "384-bit"),
    ("SHA-512",      re.compile(r"^[a-f0-9]{128}$", re.I), "512-bit"),
    ("CRC32",        re.compile(r"^[a-f0-9]{8}$", re.I), "checksum, NOT cryptographic"),
    ("NTLM / MD4",   re.compile(r"^[a-f0-9]{32}$", re.I), "same length as MD5"),
]


def sniff(h):
    h = h.strip()
    matches = [(name, note) for name, rx, note in SIGNATURES if rx.match(h)]
    return matches


def main():
    ap = argparse.ArgumentParser(description="🐾 packet-paws :: hash shape sniffer")
    ap.add_argument("hash", help="the hash string to classify")
    args = ap.parse_args()

    matches = sniff(args.hash)
    if not matches:
        print("😿 no known shape matched — could be truncated, encoded, or salted.")
        return

    print(f"🧬 candidate types for a {len(args.hash.strip())}-char string:\n")
    for name, note in matches:
        print(f"  [✓] {name:<14} — {note}")
    if len(matches) > 1:
        print("\n🐈 note: length alone is ambiguous. context (source, salt) decides.")


if __name__ == "__main__":
    main()
