import re
from tech_news.database import db


# Requisito 7
def search_by_title(title):
    news_filtered_list = []
    case_insensitive_title = re.compile(title, re.IGNORECASE)
    for news in db.news.find(
        {"title": {"$regex": case_insensitive_title}},
        {"_id": 0, "title": 1, "url": 1},
    ):
        for key, value in news.items():
            if key == "title":
                new_tuple = value, news["url"]
                news_filtered_list.append(new_tuple)
    return news_filtered_list


# Requisito 8
def search_by_date(date):
    """Seu código deve vir aqui"""
    raise NotImplementedError


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
    raise NotImplementedError
