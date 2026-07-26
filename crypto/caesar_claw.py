#!/usr/bin/env python3
"""
caesar_claw.py — 🔐 the humble Caesar cipher, with claws

Teaches: modular arithmetic, character math, brute-forcing a tiny keyspace.
A classic warm-up for the crypto category of any CTF.

Examples:
    python3 caesar_claw.py -s 3 "The cat knows"          # encode with shift 3
    python3 caesar_claw.py -s 3 -d "Wkh fdw nqrzv"       # decode with shift 3
    python3 caesar_claw.py --brute "Wkh fdw nqrzv"        # try all 26 shifts
"""
import argparse
import string


def shift_text(text, key):
    """Shift only ASCII letters by `key`, preserve everything else."""
    out = []
    for ch in text:
        if ch in string.ascii_lowercase:
            out.append(chr((ord(ch) - ord("a") + key) % 26 + ord("a")))
        elif ch in string.ascii_uppercase:
            out.append(chr((ord(ch) - ord("A") + key) % 26 + ord("A")))
        else:
            out.append(ch)
    return "".join(out)


# Tiny English-likeness score: count common letters to auto-rank brute results.
COMMON_LETTERS = set("etaoinshrdlu")


def englishness(text):
    letters = [c for c in text.lower() if c.isalpha()]
    if not letters:
        return 0.0
    hits = sum(1 for c in letters if c in COMMON_LETTERS)
    return hits / len(letters)


def main():
    ap = argparse.ArgumentParser(description="🐾 packet-paws :: Caesar cipher claw")
    ap.add_argument("text", help="text to transform")
    ap.add_argument("-s", "--shift", type=int, default=3, help="shift key (0-25)")
    ap.add_argument("-d", "--decode", action="store_true", help="decode instead of encode")
    ap.add_argument("--brute", action="store_true", help="try every shift, ranked by englishness")
    args = ap.parse_args()

    if args.brute:
        print("🔎 brute-forcing all 26 shifts (best guesses first):\n")
        ranked = sorted(
            ((k, shift_text(args.text, -k)) for k in range(26)),
            key=lambda kv: englishness(kv[1]),
            reverse=True,
        )
        for key, guess in ranked:
            print(f"  shift {key:>2}: {guess}")
        return

    key = -args.shift if args.decode else args.shift
    print(shift_text(args.text, key))


if __name__ == "__main__":
    main()
