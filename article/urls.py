from django.urls import path

from .views import ArticleList, article_comment, article_detail, share_article

app_name = "article"

urlpatterns = [
    path("", ArticleList.as_view(), name="article_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:slug>/",
        article_detail,
        name="article_detail",
    ),
    path("<int:article_id>/share/", share_article, name="article_share"),
    path("<int:article_id>/comment/", article_comment, name="comment"),
]
