from unittest.mock import Mock, patch

import pytest
from tech_news.analyzer.reading_plan import ReadingPlanService
import json


def test_reading_plan_group_news():
    json_mock = open("tests/assets/cached_news.json")
    json_data_mock = json.load(json_mock)[:2]
    mock_find_news = Mock(return_value=json_data_mock)

    with pytest.raises(ValueError):
        ReadingPlanService.group_news_for_available_time(-3)

    with patch(
        "tech_news.analyzer.reading_plan.ReadingPlanService._db_news_proxy",
        mock_find_news,
    ):
        result = ReadingPlanService.group_news_for_available_time(3)

    title_line_1 = (
        "Orkut voltou: o que se sabe até agora sobre o retorno da rede"
    )
    title_line_2 = "Oratória: passo a passo para falar bem e se destacar!"
    assert result == {
        "readable": [],
        "unreadable": [
            ("Oratória: passo a passo para falar bem e se destacar!", 15),
            (title_line_1, 4),
        ],
    }
    with patch(
        "tech_news.analyzer.reading_plan.ReadingPlanService._db_news_proxy",
        mock_find_news,
    ):
        result = ReadingPlanService.group_news_for_available_time(20)

    assert result == {
        "readable": [
            {
                "unfilled_time": 1,
                "chosen_news": [
                    (title_line_2, 15),
                    (title_line_1, 4),
                ],
            },
        ],
        "unreadable": [],
    }
