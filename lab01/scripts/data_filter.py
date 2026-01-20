import os
import csv
from bs4 import BeautifulSoup

RAW_HTML = os.path.join("../data", "raw_data", "web_data.html")
OUT_DIR = os.path.join("../data", "processed_data")
NEWS_CSV = os.path.join(OUT_DIR, "news_data.csv")
MARKET_CSV = os.path.join(OUT_DIR, "market_data.csv")

def load_soup(path):
    with open(path, "r", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")


def write_csv(path, rows, cols):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def get_latest_news(soup):
    rows = []
    ul = soup.find("ul", class_="LatestNews-list")
    if not ul:
        return rows

    for li in ul.find_all("li", class_="LatestNews-item"):
        a = li.find("a", class_="LatestNews-headline")
        t = li.find("time", class_="LatestNews-timestamp")
        if not (a and t):
            continue

        title = a.get("title") or a.get_text(strip=True)
        link = a.get("href") or ""

        rows.append(
            {
                "timestamp": t.get_text(strip=True),
                "title": title.strip(),
                "link": link.strip(),
            }
        )

    return rows


def parse_number(s):
    if s is None:
        return ""
    s = s.strip().replace(",", "")
    try:
        return float(s)
    except Exception:
        return s


def get_market_cards(soup):
    rows = []
    box = soup.find(class_=lambda c: isinstance(c, str) and "MarketsBanner" in c)
    if not box:
        return rows

    for a in box.find_all("a", class_=lambda c: isinstance(c, str) and "MarketCard-container" in c):
        sym = a.find("span", class_=lambda c: isinstance(c, str) and "MarketCard-symbol" in c)
        pos = a.find("span", class_=lambda c: isinstance(c, str) and "MarketCard-stockPosition" in c)
        chg = a.find("span", class_=lambda c: isinstance(c, str) and ("MarketCard-changePct" in c or "MarketCard-changesPts" in c))

        if not (sym and pos and chg):
            continue

        rows.append(
            {
                "symbol": sym.get_text(strip=True),
                "stock_position": parse_number(pos.get_text()),
                "change": chg.get_text(strip=True),
            }
        )
    return rows


def main():
    print("Reading HTML ...")
    soup = load_soup(RAW_HTML)

    print("Filtering fields ...")
    news = get_latest_news(soup)
    market = get_market_cards(soup)

    print("Storing Market data ...")
    write_csv(MARKET_CSV, market, ["symbol", "stock_position", "change"])
    print("CSV created:", MARKET_CSV, "rows=", len(market))

    print("Storing News data ...")
    write_csv(NEWS_CSV, news, ["timestamp", "title", "link"])
    print("CSV created:", NEWS_CSV, "rows=", len(news))

    print("Done.")


if __name__ == "__main__":
    main()
