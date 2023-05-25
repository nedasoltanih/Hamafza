from .models import Author, Badge, Article, Image
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer


class AuthorSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['age', 'about', 'image']


class BadgeSerializer(ModelSerializer):
    class Meta:
        model = Badge
        fields = ['text']


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ['path', 'featured']


class ArticleSerializer(HyperlinkedModelSerializer):
    badge = BadgeSerializer(many=True, read_only=True)
    image_set = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'published', 'publish_date', 'badge', 'image_set']
