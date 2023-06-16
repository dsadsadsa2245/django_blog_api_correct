from django.db import models
from random import randint
from category.models import Category


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    owner = models.ForeignKey('auth.user', related_name='posts',
                              on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='posts', null=True)
    preview = models.ImageField(upload_to='images/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.owner} - {self.title[:25]}'

    class Meta:
        # задает порядок сортровки постов в базе данных. внашем примере сортировка идет по created_at
        ordering = ('created_at',)


class PostImage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='images/')
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)

    def generate_name(self):
        return 'image' + str(self.id) + str(randint(100_000, 999_999))

    def save(self, *args, **kwargs):
        self.title = self.generate_name()
        return super(PostImage, self).save(*args, **kwargs)
