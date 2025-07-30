import pytest
from article.views import share_article, article_comment
from article.models import Article, Category, Comment
from django.urls import reverse


@pytest.mark.django_db
def test_article_list_view(client, published_article):
    """Проверяем, что список статей отображается и содержит опубликованные статьи."""
    url = reverse('article:article_list')
    response = client.get(url)

    assert response.status_code == 200
    assert 'articles' in response.context
    assert published_article in response.context['articles']
    assert published_article.title in response.content.decode()

@pytest.mark.django_db
def test_article_detail_view(client, published_article):
    """Проверяем, что детальная страница статьи доступна."""
    # Убедимся, что у статьи есть категория
    if not published_article.category:
        published_article.category = Category.objects.create(name="General")
        published_article.save()

    url = reverse(
        'article:article_detail',
        args=[
            published_article.publish.year,
            published_article.publish.month,
            published_article.publish.day,
            published_article.slug
        ]
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.context['article'] == published_article
    assert published_article.title in response.content.decode()
