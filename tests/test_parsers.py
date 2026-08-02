"""Unit tests for the HN, Reddit and App Store parsers."""

from painscout.models import PainPoint
from painscout.sources.appstore import AppStoreSource
from painscout.sources.hackernews import HackerNewsSource
from painscout.sources.reddit import RedditSource


def test_hn_parse_multiple_hits():
    data = {
        "hits": [
            {
                "objectID": "123",
                "title": "Ask HN: What is the most annoying manual task?",
                "story_text": "I spend hours copying data between spreadsheets.",
                "created_at": "2026-01-01T00:00:00Z",
                "points": 42,
                "num_comments": 17,
            },
            {"objectID": "456", "title": "No text, only title", "story_text": None},
            {"objectID": "789"},  # no title and no text -> excluded
            {},
        ]
    }
    points = HackerNewsSource._parse(data)
    assert len(points) == 2
    assert points[0].source == "hackernews"
    assert points[0].url == "https://news.ycombinator.com/item?id=123"
    assert points[0].meta["points"] == 42


def test_hn_parse_empty():
    assert HackerNewsSource._parse({"hits": []}) == []


def test_reddit_parse():
    data = {
        "data": {
            "children": [
                {
                    "data": {
                        "title": "This SaaS billing is confusing",
                        "selftext": "I got charged twice and support won't reply.",
                        "permalink": "/r/SaaS/comments/abc/this_saas_billing/",
                        "subreddit": "SaaS",
                        "score": 12,
                        "num_comments": 5,
                        "stickied": False,
                    }
                },
                {"data": {"title": "", "selftext": "", "permalink": "", "stickied": False}},
                {"data": {"title": "Stickied mod post", "selftext": "rules", "stickied": True}},
            ]
        }
    }
    points = RedditSource._parse(data, subreddit="SaaS")
    assert len(points) == 1
    assert points[0].source == "reddit"
    assert points[0].url.startswith("https://www.reddit.com")
    assert points[0].meta["subreddit"] == "SaaS"


def test_reddit_parse_empty():
    assert RedditSource._parse({"data": {"children": []}}) == []


def test_stackexchange_parse():
    from painscout.sources.stackexchange import StackExchangeSource

    data = {
        "items": [
            {
                "question_id": 99,
                "title": "How do I automate <b>manual data entry</b>?",
                "body": "<p>I waste hours copying invoices &amp; receipts.</p>",
                "score": 25,
                "answer_count": 3,
                "tags": ["automation", "excel"],
            },
            {"question_id": 0, "title": ""},  # no title -> excluded
        ]
    }
    points = StackExchangeSource._parse(data, site="stackoverflow")
    assert len(points) == 1
    assert points[0].source == "stackexchange"
    assert points[0].title == "How do I automate manual data entry?"
    assert "invoices & receipts" in points[0].text
    assert points[0].url == "https://stackoverflow.com/q/99"
    assert points[0].meta["tags"] == ["automation", "excel"]


def test_appstore_parse_multiple_entries():
    data = {
        "feed": {
            "entry": [
                {
                    "title": {"label": "Terrible billing"},
                    "content": {"label": "Worst app ever. The subscription renews without warning."},
                    "im:rating": {"label": "1/5"},
                    "updated": {"label": "2026-02-01T00:00:00-07:00"},
                    "author": {"name": {"label": "AngryUser"}},
                    "link": {"attributes": {"href": "https://apps.apple.com/us/app/id"}},
                },
                {
                    "title": {"label": "Great app"},
                    "content": {"label": "Works fine."},
                    "im:rating": {"label": "5/5"},
                },
            ]
        }
    }
    points = AppStoreSource._parse(data)
    assert len(points) == 2
    assert points[0].meta["rating"] == 1
    assert points[0].meta["author"] == "AngryUser"
    assert points[1].meta["rating"] == 5


def test_appstore_parse_single_entry_is_dict():
    data = {
        "feed": {
            "entry": {
                "title": {"label": "Crash"},
                "content": {"label": "Keeps crashing on login."},
                "im:rating": {"label": "2/5"},
            }
        }
    }
    points = AppStoreSource._parse(data)
    assert len(points) == 1
    assert points[0].meta["rating"] == 2


def test_appstore_parse_empty():
    assert AppStoreSource._parse({"feed": {"entry": []}}) == []


def _sample_points() -> list[PainPoint]:
    return [
        PainPoint(
            source="reddit",
            title="Data entry is killing my small business",
            text="I spend 10 hours a week manually copying invoices into Excel. There has to be a better way.",
            url="https://reddit.com/r/smallbusiness/1",
        ),
        PainPoint(
            source="hackernews",
            title="Ask HN: best way to handle customer support for a solo dev?",
            text="Support emails pile up and I never reply in time. Wish there was an automated triage bot.",
            url="https://news.ycombinator.com/item?id=2",
        ),
        PainPoint(
            source="appstore",
            title="Billing nightmare",
            text="This app charged me twice and the refund process is a joke. Worst experience.",
            url="https://apps.apple.com/3",
            meta={"rating": 1},
        ),
        PainPoint(
            source="reddit",
            title="Can't find customers for my service business",
            text="Marketing is too expensive and I have no leads. Why is growing so hard?",
            url="https://reddit.com/r/Entrepreneur/4",
        ),
    ]


def test_fallback_analyzer_clusters_and_scores():
    from painscout.analyzer import fallback_analyze

    opps = fallback_analyze(_sample_points())
    assert len(opps) >= 3
    themes = [o.theme for o in opps]
    assert "automation/manual work" in themes
    assert "billing/pricing" in themes
    # Sorted by score descending
    scores = [o.score for o in opps]
    assert scores == sorted(scores, reverse=True)
    for o in opps:
        assert o.suggested_solution
        assert o.monetization
        assert o.evidence


def test_extract_json_from_noisy_response():
    from painscout.analyzer import _extract_json

    noisy = 'Sure! Here is the result: {"opportunities": [{"theme": "x"}]} Hope that helps.'
    assert _extract_json(noisy) == '{"opportunities": [{"theme": "x"}]}'


def test_opportunities_from_json():
    from painscout.analyzer import _opportunities_from_json

    data = {
        "opportunities": [
            {
                "theme": "Manual data entry",
                "pain": "People waste hours on spreadsheets.",
                "evidence": ["quote1", "quote2"],
                "sources": ["reddit"],
                "url": "https://x.com",
                "suggested_solution": "AI invoice extractor",
                "monetization": "$29/mo",
                "score": 88,
            },
            {"theme": "Bare", "score": 10},
        ]
    }
    opps = _opportunities_from_json(data, top_n=5)
    assert len(opps) == 2
    assert opps[0].theme == "Manual data entry"
    assert opps[0].score == 88
    assert opps[0].suggested_solution == "AI invoice extractor"
