from django.urls import resolve, reverse


def test_article_url_resolves():
    url = reverse("article:article_detail", args=[2025, 7, 30, "test"])
    assert resolve(url).view_name == "article:article_detail"


def test_article_list_url_resolves():
    url = reverse("article:article_list")
    assert resolve(url).view_name == "article:article_list"


def test_article_detail_api_url():
    url = reverse(
        "api_article:article_detail_api",
        args=[
            1,
        ],
    )
    assert resolve(url).view_name == "api_article:article_detail_api"


def test_article_list_api_url():
    url = reverse("api_article:article_list_api")
    assert resolve(url).view_name == "api_article:article_list_api"
