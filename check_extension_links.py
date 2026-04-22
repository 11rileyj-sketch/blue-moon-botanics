#!/usr/bin/env python3
"""
check_extension_links.py — Blue Moon Botanics maintenance script

Validates all URLs in land_grant_extensions.json by checking HTTP status codes.
Run quarterly (or on deploy) to catch university site reorganizations.

Usage:
    python check_extension_links.py
    python check_extension_links.py --json          # machine-readable output
    python check_extension_links.py --lenient       # treat 403 as warnings, not failures
    python check_extension_links.py --path /custom/path/to/land_grant_extensions.json

Exit codes:
    0 = all links healthy
    1 = one or more broken links detected
    2 = script error (file not found, JSON parse failure, etc.)
"""

import argparse
import json
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    print("ERROR: 'requests' package required. Install with: pip install requests")
    sys.exit(2)


# Reasonable defaults for extension sites (some are slow)
TIMEOUT = 15
MAX_RETRIES = 2
RETRY_DELAY = 3
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

# Status buckets
OK_CODES = range(200, 400)  # 2xx and 3xx (redirects are fine)


def load_extensions(path: Path) -> dict:
    """Load and validate the extensions JSON file."""
    if not path.exists():
        print(f"ERROR: File not found: {path}")
        sys.exit(2)

    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {path}: {e}")
        sys.exit(2)

    # Strip metadata keys
    return {k: v for k, v in data.items() if not k.startswith("_")}


def check_url(url: str, session: requests.Session) -> dict:
    """
    Check a single URL. Returns a result dict with:
      - url: the URL checked
      - status_code: HTTP status or None if unreachable
      - ok: bool
      - error: error message if failed, else None
      - redirect_url: final URL if redirected, else None
    """
    result = {
        "url": url,
        "status_code": None,
        "ok": False,
        "error": None,
        "redirect_url": None,
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = session.head(url, timeout=TIMEOUT, allow_redirects=True)

            result["status_code"] = resp.status_code
            result["ok"] = resp.status_code in OK_CODES

            # Flag significant redirects (different domain)
            if resp.url != url:
                original_domain = urlparse(url).netloc
                final_domain = urlparse(resp.url).netloc
                if original_domain != final_domain:
                    result["redirect_url"] = resp.url

            # Some servers reject HEAD, retry with GET on 405/403
            if resp.status_code in (405, 403) and attempt == 1:
                resp = session.get(
                    url, timeout=TIMEOUT, allow_redirects=True, stream=True
                )
                resp.close()
                result["status_code"] = resp.status_code
                result["ok"] = resp.status_code in OK_CODES
                if resp.url != url:
                    original_domain = urlparse(url).netloc
                    final_domain = urlparse(resp.url).netloc
                    if original_domain != final_domain:
                        result["redirect_url"] = resp.url

            return result

        except requests.exceptions.Timeout:
            result["error"] = "timeout"
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
        except requests.exceptions.ConnectionError as e:
            result["error"] = f"connection error: {e}"
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
        except requests.exceptions.RequestException as e:
            result["error"] = str(e)
            return result

    return result


def run_checks(extensions: dict, verbose: bool = True) -> list:
    """Check all URLs across all state entries. Returns list of result dicts."""
    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
    })

    results = []
    url_fields = ["url", "gardening_url"]
    total_urls = sum(
        1 for entry in extensions.values() for f in url_fields if f in entry
    )

    if verbose:
        print(f"Checking {total_urls} URLs across {len(extensions)} states...\n")

    checked = 0
    for state, entry in sorted(extensions.items()):
        for field in url_fields:
            if field not in entry:
                continue

            url = entry[field]
            checked += 1

            if verbose:
                label = "homepage" if field == "url" else "gardening"
                print(f"  [{checked:3d}/{total_urls}] {state} ({label}): ", end="", flush=True)

            result = check_url(url, session)
            result["state"] = state
            result["field"] = field
            result["name"] = entry.get("name", "")
            results.append(result)

            if verbose:
                if result["ok"]:
                    status = f"{result['status_code']} OK"
                    if result["redirect_url"]:
                        status += f" -> {result['redirect_url']}"
                    print(f"\033[32m{status}\033[0m")
                else:
                    reason = result["error"] or f"HTTP {result['status_code']}"
                    print(f"\033[31mFAILED ({reason})\033[0m")

            # Be polite to servers
            time.sleep(0.5)

    return results


def print_summary(results: list, as_json: bool = False):
    """Print a summary of the check results."""
    broken = [r for r in results if not r["ok"]]
    redirected = [r for r in results if r["ok"] and r["redirect_url"]]

    if as_json:
        output = {
            "checked": len(results),
            "healthy": len(results) - len(broken),
            "broken": len(broken),
            "redirected": len(redirected),
            "issues": [
                {
                    "state": r["state"],
                    "field": r["field"],
                    "name": r["name"],
                    "url": r["url"],
                    "status_code": r["status_code"],
                    "error": r["error"],
                }
                for r in broken
            ],
            "redirect_warnings": [
                {
                    "state": r["state"],
                    "field": r["field"],
                    "url": r["url"],
                    "redirected_to": r["redirect_url"],
                }
                for r in redirected
            ],
        }
        print(json.dumps(output, indent=2))
        return

    print("\n" + "=" * 60)
    print(f"RESULTS: {len(results)} URLs checked")
    print(f"  Healthy:    {len(results) - len(broken)}")
    print(f"  Broken:     {len(broken)}")
    print(f"  Redirected: {len(redirected)} (cross-domain)")
    print("=" * 60)

    if broken:
        print("\nBROKEN LINKS (action required):")
        print("-" * 40)
        for r in broken:
            label = "homepage" if r["field"] == "url" else "gardening"
            reason = r["error"] or f"HTTP {r['status_code']}"
            print(f"  {r['state']} ({label}): {r['url']}")
            print(f"    {r['name']}")
            print(f"    Reason: {reason}")
            print()

    if redirected:
        print("\nCROSS-DOMAIN REDIRECTS (review recommended):")
        print("-" * 40)
        for r in redirected:
            label = "homepage" if r["field"] == "url" else "gardening"
            print(f"  {r['state']} ({label}):")
            print(f"    From: {r['url']}")
            print(f"    To:   {r['redirect_url']}")
            print()

    if not broken and not redirected:
        print("\nAll links are healthy. Nice.\n")


def main():
    parser = argparse.ArgumentParser(
        description="Validate URLs in land_grant_extensions.json"
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=Path(__file__).parent / "land_grant_extensions.json",
        help="Path to the extensions JSON file",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON (for CI/automation)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-URL output, show summary only",
    )
    parser.add_argument(
        "--lenient",
        action="store_true",
        help="Treat 403 as warnings (university WAFs often block scripts). "
             "Only truly dead links (404, 5xx, timeouts) cause exit code 1.",
    )
    args = parser.parse_args()

    extensions = load_extensions(args.path)
    results = run_checks(extensions, verbose=not args.quiet and not args.json)
    print_summary(results, as_json=args.json)

    broken = [r for r in results if not r["ok"]]
    if args.lenient:
        # In lenient mode, 403s are warnings (WAF), not failures
        truly_broken = [r for r in broken if r["status_code"] != 403]
        waf_blocked = [r for r in broken if r["status_code"] == 403]
        if waf_blocked and not args.json:
            print(f"  (--lenient: {len(waf_blocked)} 403s treated as WAF warnings, not failures)\n")
        sys.exit(1 if truly_broken else 0)
    else:
        sys.exit(1 if broken else 0)


if __name__ == "__main__":
    main()
