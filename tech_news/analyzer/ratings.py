from tech_news.database import db
from collections import Counter


# Requisito 10
def top_5_categories():
    top_5_categories_list = []
    categories_list = []
    for category in db.news.find({}, {"_id": 0, "category": 1}):
        categories_list.append((category["category"]))
    categories_counter = Counter(categories_list)
    categories_top_5 = sorted(
        categories_counter.most_common(5), key=lambda item: (-item[1], item[0])
    )
    top_5_categories_list = [
        k for k, v in categories_top_5 if categories_top_5.index((k, v)) < 5
    ]
    return top_5_categories_list
