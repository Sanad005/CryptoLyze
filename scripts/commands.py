import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Identify and attempt to crack hashes/ciphers."
    )
    parser.add_argument(
        "--wordlist",
        type=str,
        default="/usr/share/wordlists/rockyou.txt",
        help="Path to the wordlist file used for cracking (default: rockyou.txt)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="Max seconds to spend cracking before giving up (default: 15)"
    )
    parser.add_argument(
        "hash",
        type=str,
        nargs="?",           
        help="The hash or cipher text to identify (optional — will prompt if omitted)"
    )
    return parser.parse_args()