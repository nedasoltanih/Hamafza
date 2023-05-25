from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(blank=True, null=True)
    about = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(verbose_name='Profile Image', default='resources/profile_img/unknown.jpg')

    def __str__(self):
        """
        overrides the str method to show first name and last name
        @return: str
        """
        return self.user.first_name + " " + self.user.last_name


class Badge(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        """
        overrides the str method to show the text of the badge in admin panel
        @return: str
        """
        return self.text


class Article(models.Model):
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=500)
    content = models.TextField()
    published = models.BooleanField(choices=((True, 'Published'), (False, 'draft')))
    creation_date = models.DateTimeField(default=now())
    edit_date = models.DateTimeField(default=now())
    publish_date = models.DateTimeField(null=True, blank=True)
    badge = models.ManyToManyField(Badge)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        """
        overrides the save method in order to set creation date and edit date of the article to now
        """
        if not self.id:
            self.creation_date = now()
        self.edit_date = now()
        return super().save(*args, **kwargs)


class Image(models.Model):
    path = models.ImageField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    featured = models.BooleanField(verbose_name='Featured Photo', default=False)
