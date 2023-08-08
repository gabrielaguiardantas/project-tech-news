import requests
import time
import re
from tech_news.database import create_news
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
    url = "https://blog.betrybe.com"
    i = 2
    news_link_list = []
    news_list = []
    while len(news_link_list) < amount:
        html_content = fetch(url)
        if html_content:
            news_link_list += scrape_updates(html_content)
            url = "https://blog.betrybe.com"
            next_page = f"/page/{i}/"
            url = url + next_page
            i += 1
        else:
            break
    for link in news_link_list[:amount]:
        html_content = fetch(link)
        if html_content:
            news_list.append(scrape_news(html_content))
    create_news(news_list)
    return news_list
