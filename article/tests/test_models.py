import pytest

from article.models import Article, Category, Comment


@pytest.mark.django_db
def test_article_str_representation():
    """Проверяем строковое представление статьи."""
    article = Article(title="My Article")
    assert str(article) == "My Article"


@pytest.mark.django_db
def test_article_get_absolute_url(published_article):
    """Проверяем, что get_absolute_url возвращает правильный URL."""
    article = published_article
    expected_url = (f"/{article.publish.year}/"
                    f"{article.publish.month}/"
                    f"{article.publish.day}/"
                    f"{article.slug}/")
    assert article.get_absolute_url() == expected_url


@pytest.mark.django_db
def test_article_published_manager(published_article, draft_article):
    """Проверяем, что менеджер
    published возвращает только опубликованные статьи."""
    assert published_article in Article.published.all()
    assert draft_article not in Article.published.all()
    assert Article.published.count() == 1


@pytest.mark.django_db
def test_category_str_representation():
    """Проверяем строковое представление категории."""
    category = Category(name="Category")
    assert str(category) == "Category"


@pytest.mark.django_db
def test_comment_str_representation(published_article):
    comment = Comment(name="Nick")
    comment.article = published_article
    assert str(comment) == "Comment by Nick on Test Article."


@pytest.mark.django_db
def test_comment_get_absolute_url(activ_comment):
    comment = activ_comment
    expected_url = f"/{comment.id}/comment/"
    assert comment.get_absolute_url() == expected_url
