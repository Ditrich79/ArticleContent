from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .forms import EmailArticleForm, CommentModelForm
from article.models import Article, Category
from django.core.mail import send_mail
from django.utils import timezone
from django.views.decorators.http import require_POST
from rest_framework.views import APIView
from article.api.serializers import ArticleModelSerializer, CategoryModelSerializer
from rest_framework.response import Response
from rest_framework import status


def article_detail(request, slug, year, month, day):
    article = get_object_or_404(
        Article,
        slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        status=Article.Status.PUBLISHED
    )
    comments = article.comments.filter(is_active=True)
    form = CommentModelForm()
    return render(
        request,
        'article/article_detail.html',
        {'article': article, 'comments': comments, 'form': form}
    )

class ArticleList(ListView):
    model = Article
    paginate_by = 3
    template_name = 'article/articles_list.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        return context


def share_article(request, article_id):
    article = get_object_or_404(Article, id=article_id, status=Article.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailArticleForm(request.POST, initial={'published': timezone.now()})
        if form.is_valid():
            cd = form.cleaned_data
            article_url = request.build_absolute_uri(article.get_absolute_url())
            subject = (
                f"{cd['name']} ({cd['from_email']}) "
                f"recommends you read the following {article.title}"
            )
            message = (
                f"Read {article.title} at {article_url}\n\n"
                f"{cd['name']}\'s comments {cd['message']}"
                f"{cd['published']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to_email']]
            )
            sent = True
    else:
        form = EmailArticleForm()

    return render(
        request,
        'article/share_article.html',
        {
            'article': article,
            'form': form,
            'sent': sent
        }
    )


@require_POST
def article_comment(request, article_id):
    """
This function returns article's comment.
    :param request:
    :param article_id:
    :return:
    """
    article = get_object_or_404(
        Article,
        id=article_id,
        status=Article.Status.PUBLISHED
    )
    comment = None
    form = CommentModelForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.save()

    return render(
        request,
        'article/comment_article.html',
        {
            'article': article,
            'form': form,
            'comment': comment
        }
    )

class ArticleApiDetail(APIView):
    def get_instance(self, pk):
        try:
            return Article.objects.get(id=pk, status=Article.Status.PUBLISHED)
        except Article.DoesNotExist:
            raise Http404("Object does not exist.")

    def get(self, request, pk=None):
        if pk is not None:
            obj = self.get_instance(pk)
            serializer = ArticleModelSerializer(obj)
            return Response(serializer.data)
        else:
            objects = Article.published.all()
            serializer = ArticleModelSerializer(objects, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = ArticleModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        obj = self.get_instance(pk)
        serializer = ArticleModelSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        obj = self.get_instance(pk)
        serializer = ArticleModelSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_instance(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryApiDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(Category, pk=pk)

    def get(self, request, pk=None):
        if pk is not None:
            object_cat = self.get_object(pk)
            serializer = CategoryModelSerializer(object_cat)
            return serializer.data
        else:
            objects = Category.objects.all()
            serializer = CategoryModelSerializer(objects, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = CategoryModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = CategoryModelSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        obj = self.get_object(pk)
        serializer = CategoryModelSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)