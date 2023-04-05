from django.db import models
from datetime import datetime
from .resources import CHOICES, news, article
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        articles = Post.objects.filter(author=self)
        articles_rating = articles.aggregate(Sum('post_rating')).get('post_rating__sum')
        comments = Comment.objects.filter(user=self.user)
        comments_rating = comments.aggregate(Sum('comment_rating')).get('comment_rating__sum')
        comments_to_author = Comment.objects.filter(user_id=self.user)
        to_author_rating = comments_to_author.aggregate(Sum('comment_rating'))['comment_rating__sum']
        total_rating = articles_rating * 3 + comments_rating + to_author_rating
        self.user_rating = total_rating
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.category_name.title()}'

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    selection_field = models.CharField(max_length=10, choices=CHOICES, default=news)
    time_in = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through="PostCategory")
    header_field = models.CharField(max_length=255)
    text_field = models.TextField()
    post_rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.header_field.title()}: {self.text_field.title()}'

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        if len(self.text_field) > 124:
            return self.text_field[:124] + "..."
        else:
            return self.text_field


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(default="comment")
    time_in = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()