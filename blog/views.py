from django.db.models import Q, Count
from django.http import JsonResponse
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, \
    get_object_or_404, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response

from .models import Author, Badge, Article, Image
from .serializers import AuthorSerializer, BadgeSerializer, ArticleSerializer, ImageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.timezone import now


def save_article(request, pk=None):
    """
    A function to save article if it is updated or created.
    @param request: request object
    @param pk: primary key of the article if it is to edited
    @return: json response
    """
    badges = request.data.pop('badge')
    images = request.data.pop('image_set')
    if pk:
        article = Article.objects.get(pk=pk)
    else:
        article = Article.objects.create(author=Author.objects.get(user=request.user.id),
                                     **request.data)
    article.badge.set([Badge.objects.get(text=badge['text'])
                       for badge in badges])
    article.save()

    for image_data in images:
        Image.objects.create(article=article, **image_data).save()

    serializer = ArticleSerializer(article, data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return JsonResponse(serializer.errors, status=400)

    for image_data in images:
        image = Image.objects.get_or_create(article=article, **image_data)
        image_serializer = ImageSerializer(image)
        if image_serializer.is_valid():
            image_serializer.save()
        else:
            return JsonResponse(serializer.errors, status=400)

    return JsonResponse(serializer.data)


class ProfileView(RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = AuthorSerializer

    def get_object(self):
        """
        overrides the parent method in order to return the current user's author
        @return: Author object
        """
        return Author.objects.get(user=self.request.user.id)


class BadgesView(ListAPIView):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    filter_backends = [SearchFilter]
    search_fields = ["title"]


class AuthorsView(ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["article__badge__text", ]
    search_fields = ["user__first_name", "user__last_name"]

    def get_queryset(self):
        """
        overrides the parent method in order to filter author's articles based on count
        @return: queryset
        """
        queryset = super().get_queryset()
        count = self.request.query_params.get('count')
        if count:
            queryset = queryset.filter(
                Q(article__published=True)
                | Q(article__publish_date__lte=now())
            ).annotate(count=Count('article')).filter(count=count)
        return queryset.distinct()


class ArticlesView(ListAPIView):
    queryset = Article.objects.filter(Q(published=True) | Q(publish_date__lte=now()))
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["publish_date", "author__user__username", "badge__text"]
    search_fields = ["title", "content"]


class ArticlesAuthorView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleSerializer

    def get_queryset(self):
        """
        overrides the parent method in order to return the current user's articles only
        @return: set of Article objects
        """
        return Article.objects.filter(author__user=self.request.user.id)

    def create(self, request, *args, **kwargs):
        """
        overrides the parent method in order to retrieve the badges before creating an article.
        This method also creates Image objects for the article.
        @raise Badge not found
        """
        return save_article(request)


class ArticleAuthorDetail(RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleSerializer

    def get_object(self):
        """
        overrides the parent method in order to return the article only if it belongs to current user
        @return: Article object
        """
        return get_object_or_404(Article, Q(author__user=self.request.user.id)
                                 & Q(id=self.kwargs.get('pk')))

    def put(self, request, *args, **kwargs):
        """
        overrides the parent method in order to retrieve the badges before creating an article.
        This method also creates Image objects for the article.
        @raise Badge not found
        """
        save_article(request, self.kwargs.get('pk'))
