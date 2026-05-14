"""
Real Product Catalog Builder for the REFIT Smart Energy Advisor
==============================================================

Purpose
-------
Builds outputs/real_product_catalog.csv from Australian retailer search pages.
The scraper is intentionally defensive: retailer HTML changes often, so if live
scraping returns too few products, it automatically writes a realistic fallback
catalog that keeps the Streamlit dashboard working for demos and supervisor review.

Run:
    python product_scraper_retail.py

Output:
    outputs/real_product_catalog.csv

Columns:
    store, category, product_name, brand, price_aud, product_url,
    annual_kwh_est, energy_rating, source_type, scraped_at
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Iterable
from urllib.parse import quote_plus

import pandas as pd

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_PATH = OUTPUT_DIR / "real_product_catalog.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15"
    ),
    "Accept-Language": "en-AU,en;q=0.9",
}

# Search URLs are used as a practical proof-of-concept. Some retailers may block
# automated requests; fallback products are therefore kept as a reliable demo layer.
RETAILER_SEARCH_URLS = {
    "JB Hi-Fi": "https://www.jbhifi.com.au/search?query={query}",
    "The Good Guys": "https://www.thegoodguys.com.au/search?text={query}",
    "Harvey Norman": "https://www.harveynorman.com.au/catalogsearch/result/?q={query}",
    "Bunnings": "https://www.bunnings.com.au/search/products?q={query}",
    "Kmart": "https://www.kmart.com.au/search/?searchTerm={query}",
}

CATEGORIES = {
    "kettle": ["kettle", "electric kettle"],
    "toaster": ["toaster"],
    "microwave": ["microwave"],
    "fridge": ["fridge", "fridge freezer"],
    "freezer": ["freezer"],
    "washing machine": ["washing machine", "front loader washing machine"],
    "dishwasher": ["dishwasher"],
    "television": ["energy efficient tv", "led tv"],
    "heater": ["panel heater", "electric heater timer"],
    "computer": ["smart powerboard", "standby powerboard"],
    "generic": ["smart plug energy monitor", "timer plug"],
}

FALLBACK_PRODUCTS = [
    # Kettles / toasters
    ["Kmart", "kettle", "1.7L Auto-Off Kettle", "Anko", 25.00, "", 32, "Efficient", "fallback"],
    ["Big W", "kettle", "Energy Efficient Kettle", "Russell Hobbs", 49.00, "", 28, "High", "fallback"],
    ["JB Hi-Fi", "kettle", "Smart Temperature Control Kettle", "Breville", 109.00, "", 24, "Premium", "fallback"],
    ["Kmart", "toaster", "Auto-Off 2 Slice Toaster", "Anko", 29.00, "", 18, "Efficient", "fallback"],
    ["Big W", "toaster", "Variable Browning Toaster", "Sunbeam", 59.00, "", 16, "High", "fallback"],
    # Microwaves
    ["The Good Guys", "microwave", "900W Efficient Microwave", "LG", 179.00, "", 82, "High", "fallback"],
    ["JB Hi-Fi", "microwave", "Compact Inverter Microwave", "Panasonic", 219.00, "", 76, "Premium", "fallback"],
    ["Kmart", "microwave", "Compact Microwave", "Anko", 99.00, "", 96, "Standard", "fallback"],
    # Fridge / freezer
    ["The Good Guys", "fridge", "Energy Efficient Fridge-Freezer", "Hisense", 699.00, "", 260, "High", "fallback"],
    ["Harvey Norman", "fridge", "Inverter Fridge-Freezer", "Samsung", 999.00, "", 220, "Premium", "fallback"],
    ["JB Hi-Fi", "fridge", "Compact Efficient Fridge", "CHiQ", 449.00, "", 285, "Standard", "fallback"],
    ["The Good Guys", "freezer", "Efficient Upright Freezer", "Westinghouse", 849.00, "", 250, "High", "fallback"],
    ["Harvey Norman", "freezer", "Low Energy Chest Freezer", "Haier", 499.00, "", 210, "Premium", "fallback"],
    # Laundry / dishwasher
    ["The Good Guys", "washing machine", "Front Load Washing Machine", "Bosch", 849.00, "", 135, "Premium", "fallback"],
    ["JB Hi-Fi", "washing machine", "Inverter Front Loader", "LG", 799.00, "", 145, "High", "fallback"],
    ["Big W", "washing machine", "Laundry Smart Timer Plug", "Generic", 29.00, "", 180, "Control", "fallback"],
    ["The Good Guys", "dishwasher", "Eco Dishwasher", "Bosch", 899.00, "", 185, "Premium", "fallback"],
    ["Harvey Norman", "dishwasher", "Efficient Dishwasher", "Fisher & Paykel", 849.00, "", 205, "High", "fallback"],
    ["Bunnings", "dishwasher", "Appliance Timer Plug", "Arlec", 24.00, "", 230, "Control", "fallback"],
    # Entertainment / computing / heater
    ["JB Hi-Fi", "television", "Energy Efficient LED TV", "TCL", 599.00, "", 95, "High", "fallback"],
    ["The Good Guys", "television", "Low Energy QLED TV", "Samsung", 899.00, "", 80, "Premium", "fallback"],
    ["Kmart", "television", "Standby Saver Powerboard", "Generic", 19.00, "", 120, "Control", "fallback"],
    ["Officeworks", "computer", "Smart Standby Powerboard", "Jackson", 39.00, "", 135, "Control", "fallback"],
    ["JB Hi-Fi", "computer", "Energy Efficient Mini PC Setup", "Generic", 699.00, "", 105, "High", "fallback"],
    ["Bunnings", "heater", "Programmable Heater Timer", "Arlec", 24.00, "", 420, "Control", "fallback"],
    ["Big W", "heater", "Timer Controlled Heater", "Dimplex", 129.00, "", 360, "High", "fallback"],
    ["Harvey Norman", "heater", "Efficient Panel Heater", "Noirot", 349.00, "", 300, "Premium", "fallback"],
    # Generic smart controls
    ["Kmart", "generic", "Smart Plug With Timer", "Generic", 19.00, "", 80, "Control", "fallback"],
    ["Bunnings", "generic", "Timer Plug / Standby Saver", "Arlec", 24.00, "", 75, "Control", "fallback"],
    ["JB Hi-Fi", "generic", "Energy Monitoring Smart Plug", "TP-Link Tapo", 29.00, "", 70, "Monitoring", "fallback"],
]


def parse_price(text: str) -> float | None:
    match = re.search(r"\$?\s*([0-9]{1,4}(?:,[0-9]{3})*(?:\.\d{2})?)", text or "")
    if not match:
        return None
    try:
        return float(match.group(1).replace(",", ""))
    except ValueError:
        return None


def guess_brand(name: str) -> str:
    known = ["Samsung", "LG", "Hisense", "Bosch", "Breville", "Panasonic", "Westinghouse", "Haier", "TCL", "Sunbeam", "Russell Hobbs", "Fisher & Paykel", "Arlec", "Anko", "CHiQ", "Noirot", "Dimplex", "TP-Link", "Tapo"]
    low = name.lower()
    for brand in known:
        if brand.lower() in low:
            return brand
    return "Unknown"


def estimate_annual_kwh(category: str, price: float | None) -> float:
    # Conservative demo estimates; replace with official energy labels if available.
    base = {
        "kettle": 30,
        "toaster": 18,
        "microwave": 90,
        "fridge": 280,
        "freezer": 250,
        "washing machine": 150,
        "dishwasher": 210,
        "television": 100,
        "heater": 360,
        "computer": 120,
        "generic": 80,
    }.get(category, 100)
    if price and price > 500:
        return round(base * 0.85, 1)
    if price and price < 50:
        return round(base * 1.05, 1)
    return float(base)


def scrape_search_page(store: str, category: str, query: str, max_items: int = 5) -> list[dict]:
    url_template = RETAILER_SEARCH_URLS.get(store)
    if not url_template:
        return []
    url = url_template.format(query=quote_plus(query))
    try:
        import requests
        from bs4 import BeautifulSoup
        response = requests.get(url, headers=HEADERS, timeout=8)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception:
        return []
    candidates = []

    # Generic extraction: look for links/cards containing a price. This avoids hardcoding
    # fragile retailer-specific class names and makes the scraper more resilient.
    for anchor in soup.find_all("a", href=True):
        text = " ".join(anchor.get_text(" ", strip=True).split())
        if len(text) < 8 or len(text) > 180:
            continue
        price = parse_price(text)
        if price is None:
            parent_text = " ".join(anchor.parent.get_text(" ", strip=True).split()) if anchor.parent else text
            price = parse_price(parent_text)
            combined_text = parent_text
        else:
            combined_text = text
        if price is None or price <= 0:
            continue
        if not any(word.lower() in combined_text.lower() for word in query.split()[:2]):
            continue
        href = anchor["href"]
        if href.startswith("/"):
            root = re.match(r"https?://[^/]+", url)
            href = (root.group(0) if root else "") + href
        product_name = re.sub(r"\$\s*[0-9,.]+", "", combined_text).strip(" -|•")[:100]
        candidates.append({
            "store": store,
            "category": category,
            "product_name": product_name,
            "brand": guess_brand(product_name),
            "price_aud": float(price),
            "product_url": href,
            "annual_kwh_est": estimate_annual_kwh(category, price),
            "energy_rating": "Scraped estimate",
            "source_type": "scraped",
            "scraped_at": datetime.now().isoformat(timespec="seconds"),
        })
        if len(candidates) >= max_items:
            break
    return candidates


def fallback_catalog() -> pd.DataFrame:
    cols = ["store", "category", "product_name", "brand", "price_aud", "product_url", "annual_kwh_est", "energy_rating", "source_type"]
    df = pd.DataFrame(FALLBACK_PRODUCTS, columns=cols)
    df["scraped_at"] = datetime.now().isoformat(timespec="seconds")
    return df


def build_product_catalog(stores: Iterable[str] | None = None, min_products: int = 20) -> pd.DataFrame:
    stores = list(stores or RETAILER_SEARCH_URLS.keys())
    rows: list[dict] = []
    for category, queries in CATEGORIES.items():
        for store in stores:
            # Use first query only for speed; you can expand this if needed.
            rows.extend(scrape_search_page(store, category, queries[0], max_items=3))

    scraped = pd.DataFrame(rows)
    fallback = fallback_catalog()
    if scraped.empty or len(scraped) < min_products:
        out = pd.concat([scraped, fallback], ignore_index=True) if not scraped.empty else fallback
    else:
        out = scraped

    out = out.drop_duplicates(subset=["store", "category", "product_name", "price_aud"], keep="first")
    out["price_aud"] = pd.to_numeric(out["price_aud"], errors="coerce")
    out["annual_kwh_est"] = pd.to_numeric(out["annual_kwh_est"], errors="coerce")
    out = out.dropna(subset=["price_aud"])
    out.to_csv(OUTPUT_PATH, index=False)
    return out


if __name__ == "__main__":
    df = build_product_catalog()
    print(f"Saved {len(df)} products to {OUTPUT_PATH}")
