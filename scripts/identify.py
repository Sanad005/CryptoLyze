from scripts.hash import hash_id
import hashlib
from hashid import HashID
hid = HashID()
from scripts.cipher import quick_encoding_check, is_hex, is_base32, is_base64, is_binary, is_url_encoded, CipherIdentifier

cipher_id = CipherIdentifier()

def identify_input(user_input, wordlist_path="/usr/share/wordlists/rockyou.txt", timeout=15):
    user_input = user_input.strip()

    id_results = list(hid.identifyHash(user_input))

    if id_results:
        print("Detected as a HASH")
        hash_id(user_input, wordlist_path=wordlist_path, timeout=timeout)
        return

    print("No hash match — checking encodings/ciphers...")

    encodings_found = quick_encoding_check(user_input)
    if encodings_found:
        print(f"Detected as ENCODING: {', '.join(encodings_found)}")
        return

    print("Checking for classical ciphers...")
    cipher_results = cipher_id.identify(user_input)
    if cipher_results:
        print("Possible cipher types:")
        for name, conf in cipher_results:
            print(f"  {name} (confidence: {conf:.2f})")
    else:
        print("Could not identify input as hash, encoding, or known cipher.")
