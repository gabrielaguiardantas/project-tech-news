import requests
import time
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
    """Seu código deve vir aqui"""
    raise NotImplementedError


# Requisito 4
def scrape_news(html_content):
    """Seu código deve vir aqui"""
    raise NotImplementedError


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
    raise NotImplementedError
