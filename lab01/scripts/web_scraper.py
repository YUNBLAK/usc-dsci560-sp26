import os
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = "https://www.cnbc.com/world/?region=world"

def make_driver():
    opt = Options()
    opt.add_argument("--headless")
    opt.add_argument("--no-sandbox")
    opt.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=opt)


def get_market_html(driver):
    driver.get(URL)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.MarketCard-container"))
    )

    soup = BeautifulSoup(driver.page_source, "html.parser")

    card = soup.find("a", class_=lambda c: isinstance(c, str) and "MarketCard-container" in c)
    if not card:
        return ""

    box = card.find_parent("section", class_=lambda c: isinstance(c, str) and "MarketsBanner" in c)
    if not box:
        box = card.find_parent("div", class_=lambda c: isinstance(c, str) and "MarketsBanner" in c)
    if not box:
        box = card.parent

    return box.prettify() if box else ""


def get_latest_news_html():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    ul = soup.find("ul", class_=lambda c: isinstance(c, str) and "LatestNews-list" in c)
    return ul.prettify() if ul else ""


def main():
    raw_dir = os.path.join("../data", "raw_data")
    os.makedirs(raw_dir, exist_ok=True)
    out_path = os.path.join(raw_dir, "web_data.html")

    driver = make_driver()
    try:
        market_html = get_market_html(driver)
        news_html = get_latest_news_html()

        if market_html == "":
            print("Market section not found.")
        if news_html == "":
            print("Latest News section not found.")

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(market_html)
            f.write("\n\n")
            f.write(news_html)

        print("Saved:", out_path)

        with open(out_path, "r", encoding="utf-8") as f:
            for _ in range(10):
                line = f.readline()
                if not line:
                    break
                

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
