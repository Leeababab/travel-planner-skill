import re
import urllib.request
import ssl
import argparse

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def verify_file_urls(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    urls = set(re.findall(r'https?://[^\s"'<>]+', content))
    print(f"Verifying {len(urls)} URLs in {file_path}...")

    failed = []
    for u in sorted(urls):
        if any(x in u for x in ["fonts.googleapis", "fonts.gstatic", "unpkg.com", "w3.org"]):
            continue
        try:
            req = urllib.request.Request(u, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=6, context=ctx) as res:
                code = res.getcode()
                if 200 <= code < 400:
                    print(f" [OK {code}] {u}")
                else:
                    print(f" [FAIL {code}] {u}")
                    failed.append((u, code))
        except Exception as e:
            print(f" [WARN/ERR] {u} -> {e}")

    print(f"URL Verification Completed. Failures: {len(failed)}")
    return len(failed) == 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify all URLs in an HTML/JSON travel file")
    parser.add_argument("--file", required=True)
    args = parser.parse_args()
    verify_file_urls(args.file)
