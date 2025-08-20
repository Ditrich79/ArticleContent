from django.urls import path

from article.views import ArticleApiDetail, CategoryApiDetail

app_name = "api_article"

urlpatterns = [
    path(
        "v1/articles/<int:pk>/",
        ArticleApiDetail.as_view(),
        name="article_detail_api"
    ),
    path("v1/articles/", ArticleApiDetail.as_view(), name="article_list_api"),
    path("v1/categories/",
         CategoryApiDetail.as_view(),
         name="category_list_api"),
]
