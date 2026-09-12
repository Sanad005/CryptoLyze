import hashlib
from hashid import HashID
from scripts.crack import crack_from_wordlist, HASHLIB_MAP

hid = HashID()

def hash_id(hash_value, wordlist_path="/usr/share/wordlists/sanad.txt", timeout=15):
    id = hid.identifyHash(hash_value)
    print("possible hash types:")
    s = 1
    candidates = list(id)[:5]
    for r in candidates:
        print("Most Likely To Be One Of This Hash Types")
        print(f"{s}.\nHash Name : {r.name}\nHashCat Code = {r.hashcat}\nJohn Code = {r.john}\n")
        s += 1

    for r in candidates:
        if r.name.upper() in HASHLIB_MAP:
            print(f"Attempting quick crack as {r.name}...")
            result = crack_from_wordlist(hash_value, r.name, wordlist_path, timeout=timeout)
            if result["cracked"]:
                print(f"✅ Cracked!\n Plaintext: {result['plaintext']} "
                      f"({result['attempts']} attempts, {result['elapsed']}s)")
                return
            else:
                print(f"❌ Not found ({result.get('reason')}, "
                      f"{result.get('attempts', 0)} attempts, {result.get('elapsed', 0)}s)")
    print("Could not crack with available wordlist in time limit.")