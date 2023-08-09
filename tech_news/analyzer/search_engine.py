import re
from tech_news.database import db
from datetime import datetime


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
    news_filtered_list = []
    if not date_validate(date):
        raise ValueError("Data inválida")
    year = int(date[:4])
    month = int(date[5:7])
    day = int(date[8:10])
    new_format_date = datetime.date(datetime(year, month, day))
    string_new_format_date = new_format_date.strftime("%d/%m/%Y")
    for news in db.news.find(
        {"timestamp": {"$regex": string_new_format_date}},
        {"_id": 0, "title": 1, "url": 1},
    ):
        for key, value in news.items():
            if key == "title":
                new_tuple = value, news["url"]
                news_filtered_list.append(new_tuple)
    return news_filtered_list


# Requisito 9
def search_by_category(category):
    news_filtered_list = []
    case_insensitive_category = re.compile(category, re.IGNORECASE)
    for news in db.news.find(
        {"category": {"$regex": case_insensitive_category}},
        {"_id": 0, "title": 1, "url": 1},
    ):
        for key, value in news.items():
            if key == "title":
                new_tuple = value, news["url"]
                news_filtered_list.append(new_tuple)
    return news_filtered_list


def year_validate(year):
    if int(year) in range(10000):
        return True
    return False


def month_and_day_validate(month, day):
    for _ in range(1, 13):
        if int(month) in [1, 3, 5, 7, 8, 10, 12] and day in range(1, 32):
            return True
        elif int(month) in [4, 6, 9, 11] and day in range(1, 31):
            return True
        else:
            if int(day) in range(1, 29):
                return True
            else:
                return False


def month_validate(month):
    if int(month) in range(1, 13):
        return True
    return False


def date_validate(date):
    """firstly verify the correct date format (YYYY-MM-DD),
    then verify if the year, month and day are valid"""
    pattern = r"\d{4}-\d{2}-\d{2}"
    if not re.match(pattern, date):
        return False
    if (
        year_validate(date[:4])
        and month_validate(date[5:7])
        and month_and_day_validate(date[5:7], date[8:10])
    ):
        return True
    return False
