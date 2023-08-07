import requests
import time
import re
from parsel import Selector


# Requisito 1
def fetch(url):
    try:
        response = requests.get(
            url, headers={"user-agent": "Fake user-agent"}, timeout=3
        )  # lança um ReadTimeout se demorar mais de 3 seg
        time.sleep(1)
        response.raise_for_status()
        return response.text
    except requests.HTTPError:
        print("HTTP ERROR")
        return None
    except requests.ReadTimeout:
        print("READ TIMEOUT")
        return None


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(html_content)
    updates = selector.css(".cs-overlay-link::attr(href)").getall()
    return updates


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    next_page_button = selector.css(".next.page-numbers::attr(href)").get()
    if next_page_button:
        return next_page_button
    return None


# Requisito 4
def scrape_news(html_content):
    selector = Selector(html_content)
    pattern = re.compile("<.*?>")
    remove_htmls = re.sub(pattern, "", selector.css("p").get())
    news = {
        "url": selector.css("[rel='canonical']::attr(href)").get(),
        "title": selector.css(".entry-title::text").get().strip(),
        "timestamp": selector.css(".meta-date::text").get(),
        "writer": selector.css(".url.fn.n::text").get(),
        "reading_time": int(
            "".join(
                filter(
                    str.isdigit, selector.css(".meta-reading-time::text").get()
                )
            )
        ),
        "summary": remove_htmls.strip(),
        "category": selector.css(".label::text").get(),
    }
    return news


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
    raise NotImplementedError
