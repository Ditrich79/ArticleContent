import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from article.models import Article, Category, Comment
from django.utils import timezone
from django.test.client import RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile


User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(username='testUser', email='test@example.com', password='testpass')

@pytest.fixture
def author(user):
    return user

@pytest.fixture
def category():
    return Category.objects.create(
        name='Test Category',
        description='Test description of category',
    )

@pytest.fixture
def published_article(author, category):
    image = SimpleUploadedFile(
        name='test_image.jpg',
        content=b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb1\x00\x00\x00\x00IEND\xaeB`\x82',
        content_type='image/jpeg'
    )
    return Article.objects.create(
        title='Test Article',
        slug='test-article',
        user=author,
        category=category,
        body='This is a test Article.',
        status=Article.Status.PUBLISHED,
        publish=timezone.now(),
        picture=image
    )

@pytest.fixture
def draft_article(author, category):
    return Article.objects.create(
        title='Draft Article',
        slug='draft-article',
        user=author,
        category=category,
        body='This is a Draft.',
        status=Article.Status.DRAFT
    )

@pytest.fixture
def activ_comment(published_article):
    return Comment.objects.create(
        name='Ditrich',
        content='This is the first test comment.',
        email='example@gmail.com',
        is_active=True,
        article=published_article
    )

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def rf():
    return RequestFactory()

@pytest.fixture
def sample_article(db):
    article = Article.objects.create(title="Test Article", status=Article.Status.PUBLISHED)
    return article