from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

article = 'ARTL'
news = 'NEWS'

CONTENT_TYPES = [(article, 'ARTL'),
                 (news, 'NEWS')]


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        cont_rating = self.post_set.aggregate(contentRating=Sum('content_rating'))
        contRat = 0
        contRat += cont_rating.get('contentRating')

        comm_rating = self.author_user.comment_set.aggregate(commentRating=Sum('comment_rating'))
        commRat = 0
        commRat += comm_rating.get('commentRating')

        self.author_rating = contRat * 3 + commRat
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    choice = models.CharField(max_length=4, choices=CONTENT_TYPES, default=article)
    register_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=100)
    content = models.TextField()
    content_rating = models.SmallIntegerField(default=0)

    def like(self):
        self.content_rating += 1
        self.save()

    def dislike(self):
        self.content_rating -= 1
        self.save()

    def preview(self):
        return f'{str(self.content)[:125].strip()}...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(blank=True)
    register_comment = models.DateTimeField(auto_now_add=True)
    comment_rating = models.SmallIntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

# Create your models here.
