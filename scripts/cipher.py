import re 
import base64
import binascii
from collections import Counter

def is_base64(text):
    text = text.strip()
    if not re.fullmatch(r'[A-Za-z0-9+/]+={0,2}', text) or len(text) % 4 != 0:
        return False
    try:
        base64.b64decode(text,validate=True)
        return True
    except Exception:
        return False
def is_base32(text):
    text = text.strip()
    if not re.fullmatch(r'[A-Z2-7]+=*', text):
        return False
    try:
        base64.b32decode(text)
        return True
    except Exception:
        return False
def is_hex(text):
    text = text.strip()
    if not re.fullmatch(r'[a-fA-F0-9]+', text) or len(text) % 2 != 0:
        return False
    try:
        binascii.unhexlify(text)
        return True
    except Exception:
        return False

def is_binary(text):
    text = text.strip().replace(" ", "")
    return bool(re.fullmatch(r'[01]+', text)) and len(text) % 8 == 0

def is_url_encoded(text):
    return bool(re.search(r'%[0-9A-Fa-f]{2}', text))

def is_rot47_candidate(text):
    printable = [c for c in text if 33 <= ord(c) <= 126]
    return len(printable) == len(text) and bool(re.search(r'[!-~]', text)) and not text.isalpha()

def quick_encoding_check(text):
    results = []
    if is_hex(text):
        results.append("Hex")
    if is_base32(text):
        results.append("Base32")
    if is_base64(text):
        results.append("Base64")
    if is_binary(text):
        results.append("Binary")
    if is_url_encoded(text):
        results.append("URL-encoded")
    return results
class CipherIdentifier:
    ENGLISH_FREQ = {
        'a': 8.2, 'b': 1.5, 'c': 2.8, 'd': 4.3, 'e': 12.7, 'f': 2.2,
        'g': 2.0, 'h': 6.1, 'i': 7.0, 'j': 0.15, 'k': 0.77, 'l': 4.0,
        'm': 2.4, 'n': 6.7, 'o': 7.5, 'p': 1.9, 'q': 0.095, 'r': 6.0,
        's': 6.3, 't': 9.1, 'u': 2.8, 'v': 0.98, 'w': 2.4, 'x': 0.15,
        'y': 2.0, 'z': 0.074
    }

    def chi_squared(self, text):
        text = ''.join(c.lower() for c in text if c.isalpha())
        if not text:
            return float('inf')
        n = len(text)
        counts = Counter(text)
        chi2 = 0
        for letter, expected_pct in self.ENGLISH_FREQ.items():
            expected = n * expected_pct / 100
            observed = counts.get(letter, 0)
            chi2 += (observed - expected) ** 2 / expected if expected else 0
        return chi2

    def caesar_shift_scan(self, text):
        letters_only = [c for c in text if c.isalpha()]
        if not letters_only:
            return None
        best_shift, best_score = None, float('inf')
        for shift in range(26):
            shifted = ''.join(
                chr((ord(c.lower()) - 97 - shift) % 26 + 97) if c.isalpha() else c
                for c in text
            )
            score = self.chi_squared(shifted)
            if score < best_score:
                best_score, best_shift = score, shift
        return {'likely_shift': best_shift, 'chi2': best_score}

    def identify(self, text):
        results = []
        if re.match(r'^[A-Za-z\s.,!?\'"-]+$', text):
            scan = self.caesar_shift_scan(text)
            if scan and scan['chi2'] < 50:
                results.append((f"Caesar/ROT (shift≈{scan['likely_shift']})", 0.85))
            else:
                results.append(('Possible Vigenère or polyalphabetic (flat letter freq)', 0.4))
        return sorted(results, key=lambda x: -x[1])