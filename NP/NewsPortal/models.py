from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        posts = Post.objects.filter(author=self)
        posts_rating = posts.aggregate(Sum('rating')).get('rating__sum')
        comments = Comment.objects.filter(user=self.user)
        comments_rating = comments.aggregate(Sum('rating')).get('rating__sum')
        comments_to_author = Comment.objects.filter(user_id=self.user)
        to_author_rating = comments_to_author.aggregate(Sum('rating')).get('rating__sum')
        total_rating = posts_rating * 3 + comments_rating * 3 + to_author_rating * 3
        self.rating = total_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscribers')


class Post(models.Model):
    CHOICE = [
        ('news', 'новости'),
        ('article', 'статья')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    choice = models.CharField(max_length=10, choices=CHOICE, default='news')
    time_in = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.content}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[:124] + '...'


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
