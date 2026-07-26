<div align="center">

# 🐾 packet-paws

*small security scripts with sharpened claws*

<img src="https://img.shields.io/badge/purpose-learning%20%26%20labs-00ff41?style=flat-square" alt="purpose" />
<img src="https://img.shields.io/badge/supervised%20by-cat.exe-0d1117?style=flat-square" alt="cat" />
<img src="https://img.shields.io/badge/language-Python%203-3776ab?style=flat-square" alt="python" />

</div>

## 📖 What is this?

A growing litter of **tiny, readable security scripts** I write while learning offensive & defensive fundamentals. Each one is small enough to read in a sitting, commented for study, and built to teach a single concept.

> 「A hunter sharpens claws on wood before the hunt — never on the innocent.」

## 🐈 The Litter

| Script | Claw | What it teaches |
|---|---|---|
| `recon/port_peek.py` | 🔎 | TCP connect scanning & sockets |
| `crypto/caesar_claw.py` | 🔐 | classical cipher shift/brute-force |
| `hashing/hash_sniffer.py` | 🧬 | identifying hashes by shape |
| `net/http_pounce.py` | 📡 | HTTP headers & security-header audit |

## 🚀 Usage

Each script is standalone and uses only the Python 3 standard library:

```bash
python3 recon/port_peek.py 127.0.0.1 -p 20-100
python3 crypto/caesar_claw.py --brute "Wkh fdw nqrzv"
python3 hashing/hash_sniffer.py 5d41402abc4b2a76b9719d911017c592
python3 net/http_pounce.py https://example.com
```

## 🐾 House Rules

- **Learning & authorized labs only.** Only point these at systems you own or have **explicit written permission** to test.
- No exploitation payloads live here — these are recon/learning primitives.
- Unauthorized scanning or access is illegal. The cat does not bail you out. 🐈‍⬛

## ⚖️ License

[MIT](./LICENSE) — use freely, blame no cat.

---

<div align="center">

*cat.exe is watching your packets. purring on port 22.*

</div>
