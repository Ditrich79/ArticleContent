import pytest
from article.forms import EmailArticleForm, CommentModelForm


def test_email_form_valid():
    email_form = EmailArticleForm(data={
        'name': 'Rosenbaum',
        'from_email': 'example@gmail.com',
        'to_email': 'anybody@gmail.com',
        'message': 'Hello, this is the first test message',
        'published': '2025-07-29'
    })
    assert email_form.is_valid()

def test_email_form_invalid():
    email_form = EmailArticleForm(data={})
    assert not email_form.is_valid()
    assert 'name' in email_form.errors
    assert 'from_email' in email_form.errors
    assert 'to_email' in email_form.errors

def test_comment_form_valid():
    comment_form = CommentModelForm(data={
        'name': 'Alice',
        'email': 'example@gmail.com',
        'content': 'Hello, this is the second test message'
    })
    assert comment_form.is_valid()

def test_comment_form_invalid():
    comment_form = CommentModelForm(data={
        'name': 263,
        'email': True,
        'content': 65.23
    })
    assert not comment_form.is_valid()