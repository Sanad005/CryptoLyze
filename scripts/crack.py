import hashlib
import time

HASHLIB_MAP = {
    "MD5": "md5",
    "SHA-1": "sha1",
    "SHA-224": "sha224",
    "SHA-256": "sha256",
    "SHA-384": "sha384",
    "SHA-512": "sha512",
    "MD4": "md4",  
}

def hash_word(word, algo):
    algo = algo.lower()
    try:
        h = hashlib.new(algo)
    except ValueError:
        return None 
    h.update(word.encode(errors="ignore"))
    return h.hexdigest()

def crack_from_wordlist(target_hash, hash_name, wordlist_path, timeout=15, encoding="latin-1"):
    
    algo = HASHLIB_MAP.get(hash_name.upper())
    if algo is None:
        return {"cracked": False, "reason": f"No hashlib support for {hash_name}"}

    target_hash = target_hash.strip().lower()
    start = time.time()
    attempts = 0

    try:
        with open(wordlist_path, "r", encoding=encoding, errors="ignore") as f:
            for line in f:
               
                if time.time() - start > timeout:
                    return {
                        "cracked": False,
                        "reason": "timeout",
                        "attempts": attempts,
                        "elapsed": round(time.time() - start, 2)
                    }

                word = line.rstrip("\n").rstrip("\r")
                if not word:
                    continue

                attempts += 1
                candidate = hash_word(word, algo)

                if candidate == target_hash:
                    return {
                        "cracked": True,
                        "plaintext": word,
                        "attempts": attempts,
                        "elapsed": round(time.time() - start, 2)
                    }

    except FileNotFoundError:
        return {"cracked": False, "reason": f"Wordlist not found: {wordlist_path}"}

    return {
        "cracked": False,
        "reason": "exhausted wordlist",
        "attempts": attempts,
        "elapsed": round(time.time() - start, 2)
    }