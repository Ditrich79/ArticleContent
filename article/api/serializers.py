from rest_framework import serializers

from article.models import Article, Category


class ArticleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["id", "title", "body", "status", "publish", "picture"]


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]
