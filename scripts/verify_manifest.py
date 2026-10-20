"""Check files against a MANIFEST.sha256 (cross-platform replacement for `sha256sum -c`).

python scripts/verify_manifest.py MANIFEST.sha256 [root]
Each manifest line is "<sha256>  <relative path>". Text files are compared after normalising CRLF to LF, so a checkout made
with Windows line-ending conversion still verifies; binary files are compared byte for byte. Exit status 0 only if every
listed file exists and matches.
"""
import hashlib
import os
import sys

TEXT = (".md", ".csv", ".json", ".jsonl", ".txt", ".py", ".html", ".cff", ".sha256", ".gitattributes", "LICENSE")


def digest(path):
    b = open(path, "rb").read()
    if path.endswith(TEXT) or os.path.basename(path) in TEXT:
        b = b.replace(b"\r\n", b"\n")
    return hashlib.sha256(b).hexdigest()


def main():
    manifest = sys.argv[1] if len(sys.argv) > 1 else "MANIFEST.sha256"
    root = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(manifest))
    bad = missing = n = 0
    for line in open(manifest, encoding="utf-8"):
        if not line.strip():
            continue
        h, rel = line.rstrip("\n").split("  ", 1)
        path = os.path.join(root, rel)
        n += 1
        if not os.path.exists(path):
            missing += 1; print("MISSING", rel)
        elif digest(path) != h:
            bad += 1; print("MISMATCH", rel)
    print(f"{n - bad - missing} / {n} files match" + (f"; {bad} mismatching, {missing} missing" if bad or missing else ""))
    sys.exit(1 if bad or missing else 0)


if __name__ == "__main__":
    main()
