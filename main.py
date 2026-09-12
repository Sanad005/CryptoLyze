import hashlib
from hashid import HashID
from scripts.identify import identify_input
from scripts.commands import parse_args
import os
def resolve_wordlist_path(path):
    if os.path.isabs(path):
        return path
    project_root = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(project_root, path)
def main():
    args = parse_args()
    args.wordlist = resolve_wordlist_path(args.wordlist)

    if args.hash:
        c = args.hash
    else:
        c = input("enter hash or cipher: ")

    identify_input(c, wordlist_path=args.wordlist, timeout=args.timeout)

if __name__ == "__main__":
    main()