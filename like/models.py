from django.db import models

from posts.models import Post


# Create your models here.
class Like(models.Model):
    owner = models.ForeignKey('auth.User', related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        # делает так чтобы один owner не мог поставить лайк два раза одному посту.
        # owner id = 7      post id=15 --- можно
        #   owner id=7    post id = 16 ----- можно
        #   owner id =7 post id =15 ---- нельзя
        unique_together = ['owner', 'post']


class Favorite(models.Model):
    owner = models.ForeignKey('auth.User', related_name='favorites', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        unique_together = ['owner', 'post']
