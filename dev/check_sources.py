"""Fetch every URL in the plant library and list the ones that fail.

    python dev/check_sources.py

Some sites block scripts (Bunnings, Agriculture Victoria and NSW DPI answer 403). Those are listed as blocked,
not broken: open them in a browser to confirm.
"""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
import urllib.error
import urllib.request

import yaml

DATA = Path(__file__).resolve().parents[1] / "custom_components/cyborg_gardening/library/data"
BLOCKERS = ("bunnings.com.au", "agriculture.vic.gov.au", "dpi.nsw.gov.au", "dpird.nsw.gov.au")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36"


def urls(value, found: dict, where: str) -> None:
    if isinstance(value, dict):
        for key, val in value.items():
            urls(val, found, where)
    elif isinstance(value, list):
        for val in value:
            urls(val, found, where)
    elif isinstance(value, str) and value.startswith("https://"):
        found.setdefault(value, set()).add(where)


def check(url: str) -> tuple[str, str]:
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(request, timeout=25) as response:  # noqa: S310
            return url, str(response.status)
    except urllib.error.HTTPError as err:
        return url, str(err.code)
    except Exception as err:  # noqa: BLE001
        return url, type(err).__name__


found: dict[str, set[str]] = {}
for path in sorted(DATA.rglob("*.yaml")):
    urls(yaml.safe_load(path.read_text(encoding="utf-8")), found, str(path.relative_to(DATA)))

with ThreadPoolExecutor(12) as pool:
    results = sorted(pool.map(check, found))

broken = [(u, s) for u, s in results if not s.startswith(("2", "3"))]
blocked = [(u, s) for u, s in broken if any(b in u for b in BLOCKERS)]
broken = [(u, s) for u, s in broken if (u, s) not in blocked]
print(f"{len(results)} URLs, {len(broken)} broken, {len(blocked)} blocked by the site")
for url, status in broken:
    print(f"BROKEN {status} {url}  <- {', '.join(sorted(found[url]))}")
for url, status in blocked:
    print(f"BLOCKED {status} {url}")
sys.exit(1 if broken else 0)
