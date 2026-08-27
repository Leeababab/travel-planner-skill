import os
import time
import urllib.request
import ssl
import argparse

USER_AGENT = "AntigravityTravelPlanner/1.0 (https://github.com/Leeababab/travel-planner-skill)"
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".tile_cache")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_tile(z, x, y, cache_dir=CACHE_DIR):
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, f"{z}_{x}_{y}.png")
    if os.path.exists(cache_path):
        return cache_path

    url = f"https://a.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
                if resp.getcode() == 200:
                    with open(cache_path, "wb") as f:
                        f.write(resp.read())
                    return cache_path
        except Exception as e:
            time.sleep(2 ** attempt)

    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch CartoDB map tile with caching.")
    parser.add_argument("--z", type=int, default=7)
    parser.add_argument("--x", type=int, default=126)
    parser.add_argument("--y", type=int, default=80)
    parser.add_argument("--cache-dir", type=str, default=CACHE_DIR)
    args = parser.parse_args()

    tile = get_tile(args.z, args.x, args.y, args.cache_dir)
    print(f"Tile cached at: {tile}")
