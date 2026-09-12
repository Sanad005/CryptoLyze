# CryptoLyze

A Python CLI tool that identifies hash types and classical ciphers, then automatically attempts to crack identified hashes using a wordlist — all locally, with no external API calls or paid cracking services.

> Rename this section if you go with a different project name — replace `CryptoLyze` throughout.

## Features

- **Hash identification** — detects likely hash types (MD5, SHA-1, SHA-224/256/384/512, and more) using pattern matching, and ranks candidates.
- **Automatic cracking** — once a hash type is identified, attempts a fast wordlist-based crack with a configurable timeout, so it won't hang on large wordlists.
- **Encoding detection** — recognizes common encodings: Base64, Base32, Hex, Binary, URL-encoding.
- **Classical cipher detection** — uses chi-squared frequency analysis to detect Caesar-shift ciphers and flag likely Vigenère/polyalphabetic ciphertext.
- **Configurable wordlist and timeout** via command-line flags.
- Runs entirely offline — no reliance on external services like CrackStation (which has no public API) or paid cracking APIs.

## Requirements

- Python 3.8+
- [`hashid`](https://pypi.org/project/hashID/) library

Install dependencies:

```bash
pip install hashid
```

## Project structure

```
CryptoLyze/
├── main.py                 # entry point, CLI argument handling
└── scripts/
    ├── commands.py          # argparse setup (--wordlist, --timeout, --help)
    ├── identify.py          # top-level routing: hash vs. encoding vs. cipher
    ├── hash.py              # hash identification + crack orchestration
    ├── crack.py             # wordlist-based cracking logic
    └── cipher.py            # encoding + classical cipher detection
```

## Usage

### Interactive mode

Run with no arguments and you'll be prompted:

```bash
python3 main.py
```
```
enter hash or cipher: 5f4dcc3b5aa765d61d8327deb882cf99
```

### Direct mode

Pass the hash or ciphertext as an argument:

```bash
python3 main.py 5f4dcc3b5aa765d61d8327deb882cf99
```

### Custom wordlist

```bash
python3 main.py 5f4dcc3b5aa765d61d8327deb882cf99 --wordlist /path/to/wordlist.txt
```

Relative paths are resolved relative to the project root (where `main.py` lives), not your current working directory — so `--wordlist rockyou.txt` will always look for `rockyou.txt` next to `main.py` regardless of where you run the command from.

### Custom crack timeout

By default, cracking attempts stop after 15 seconds per candidate hash type to avoid hanging on large wordlists.

```bash
python3 main.py 5f4dcc3b5aa765d61d8327deb882cf99 --wordlist rockyou.txt --timeout 30
```

### Help

```bash
python3 main.py --help
```
```
usage: main.py [-h] [--wordlist WORDLIST] [--timeout TIMEOUT] [hash]

Identify and attempt to crack hashes/ciphers.

positional arguments:
  hash                 The hash or cipher text to identify (optional — will prompt if omitted)

options:
  -h, --help           show this help message and exit
  --wordlist WORDLIST  Path to the wordlist file used for cracking (default: rockyou.txt)
  --timeout TIMEOUT    Max seconds to spend cracking before giving up (default: 15)
```

## How it works

1. **Hash check first.** The input is run through `hashid`, which pattern-matches it against known hash formats by length and charset. If any candidates are found, the tool treats the input as a hash.
2. **Crack attempt.** For each candidate hash type that Python's `hashlib` supports directly (MD5, SHA-1, SHA-224/256/384/512), the tool hashes each word in the wordlist and compares it to the target. It stops as soon as a match is found, the wordlist is exhausted, or the timeout is hit.
3. **Encoding check.** If no hash type matches, the input is checked against common encodings (Base64, Base32, Hex, Binary, URL-encoding) using format validation and successful decode tests.
4. **Classical cipher check.** If nothing else matches, the tool assumes the input might be a classical cipher. It runs a Caesar-shift scan across all 26 possible shifts, scoring each with chi-squared analysis against expected English letter frequencies. A low chi-squared score at some shift strongly suggests a Caesar cipher; a flat/uniform distribution across all shifts suggests something polyalphabetic like Vigenère.

## Limitations

- **Salted hashes** (bcrypt, MD5crypt, SHA512crypt, Argon2, etc.) are identified by prefix but not currently cracked by the wordlist cracker, since they require salt-aware hashing rather than a plain `hash(word)` comparison.
- **Cracking success depends entirely on wordlist coverage.** If the plaintext isn't in your wordlist, it won't be found — this is a fundamental limitation of dictionary attacks, not a bug.
- **Ambiguous hash lengths.** Several hash types share the same output length and charset (e.g. MD5, MD4, MD2, NTLM, and Double MD5 are all 32 hex characters), so multiple candidates may be listed for a single hash. The tool tries the most common ones first but can't definitively distinguish between them from the string alone.
- **Classical cipher detection is statistical, not certain.** Chi-squared scoring gives a best guess, not a guarantee — short ciphertext samples in particular can produce unreliable frequency analysis.



## Disclaimer

This tool is intended for educational purposes, CTF challenges, and authorized security testing only. Only use it against hashes and data you own or have explicit permission to test. Unauthorized use against systems or data you don't own or have permission to access may be illegal.


# License

MIT License

Copyright (c) 2026 Sanad005

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE
