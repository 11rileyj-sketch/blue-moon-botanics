# image_search.py
# Shared image search utility for Blue Moon Botanics.
# Used by plant_intake.py (intake pipeline) and app.py (Update Photo feature).

import os
import requests
from urllib.parse import quote

# ─── CONFIG ───────────────────────────────────────────────────────────────────
def _get_config(key):
    val = os.environ.get(key)
    if val:
        return val
    try:
        import config
        return getattr(config, key, None)
    except ImportError:
        return None

SERPER_API_KEY    = _get_config("SERPER_API_KEY")
PLACEHOLDER_PHOTO = "https://www.vecteezy.com/free-vector/potted-plant-silhouette"

# ─── LOGGING HELPER ───────────────────────────────────────────────────────────
def _log(msg, log=None):
    print(msg)
    if log is not None:
        log.append(msg)

# ─── WSRV PROXY ───────────────────────────────────────────────────────────────
def build_wsrv_url(img_url):
    """
    Safely builds a wsrv.nl proxy URL with proper encoding of the source URL.
    Skips wsrv for CDN transformation URLs that don't need proxying.
    """
    skip_domains = ['thespruce.com', 'thdstatic.com', 'shopify.com', 'squarespace.com']
    if any(domain in img_url for domain in skip_domains):
        return img_url
    encoded = quote(img_url, safe='')
    return f"https://wsrv.nl/?url={encoded}&w=800&h=800&fit=cover"

# ─── SERPER IMAGE SEARCH ──────────────────────────────────────────────────────
def search_serper_images(query, log=None):
    """Searches Google Images via Serper.dev for a plant image."""
    try:
        url     = "https://google.serper.dev/images"
        headers = {
            "X-API-KEY":    SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {"q": query, "num": 10}
        r       = requests.post(url, headers=headers, json=payload)
        data    = r.json()
        images  = data.get('images', [])
        if images:
            img_url = images[0].get('imageUrl')
            _log(f"   Serper query: '{query}' → found: {img_url}", log)
            return img_url
        else:
            _log(f"   Serper query: '{query}' → no results", log)
            return None
    except Exception as e:
        _log(f"   Serper error: {e}", log)
        return None

# ─── WIKIMEDIA IMAGE SEARCH ───────────────────────────────────────────────────
def search_wikimedia_images(query, log=None):
    """Searches Wikimedia Commons for a plant image by scientific or common name."""
    try:
        url    = "https://en.wikipedia.org/w/api.php"
        params = {
            "action":      "query",
            "titles":      query,
            "prop":        "pageimages",
            "format":      "json",
            "pithumbsize": 800,
            "redirects":   1
        }
        r    = requests.get(url, params=params,
                            headers={"User-Agent": "BlueMoonProjects-PlantIntake/2.7"})
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            thumb = page.get("thumbnail", {}).get("source")
            if thumb:
                _log(f"   Wikimedia query: '{query}' → found: {thumb}", log)
                return thumb
        _log(f"   Wikimedia query: '{query}' → no results", log)
        return None
    except Exception as e:
        _log(f"   Wikimedia error: {e}", log)
        return None

# ─── MAIN IMAGE FETCHER ───────────────────────────────────────────────────────
def get_plant_image(plant_name, common_name, scientific_name, log=None):
    """
    Search order:
    0. Serper    — raw plant_name input (best results, decoupled from scientific name)
    1. Wikimedia — scientific name (reliable, attribution-friendly)
    2. Wikimedia — common name fallback
    3. Placeholder
    """
    base_name = " ".join(scientific_name.replace("'", "").split()[:2]).strip()

    _log(f"   🔍 Trying Serper: '{plant_name} houseplant'", log)
    img = search_serper_images(f"{plant_name} houseplant", log)
    if img:
        return img

    _log(f"   🔍 Trying Wikimedia: '{base_name}'", log)
    img = search_wikimedia_images(base_name, log)
    if img:
        return img

    _log(f"   🔍 Trying Wikimedia: '{common_name}'", log)
    img = search_wikimedia_images(common_name, log)
    if img:
        return img

    _log(f"   ⚠️ No photo found. Using placeholder.", log)
    return PLACEHOLDER_PHOTO
