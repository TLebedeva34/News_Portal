from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(
        max_length=50
    )
    text = models.TextField()
    date = models.DateField(
        auto_now_add=True
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='articles',
    )
    author = models.ForeignKey(
        to='Author',
        on_delete=models.CASCADE,
        related_name='author',
    )

    def __str__(self):
        return f'{self.title.title()}: {self.text[:30]}'

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])


class Author(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return f'{self.name.title()}'


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return f'{self.name.title()}'


class CategoryArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
