from unittest.util import _MAX_LENGTH
from django.db import models
from django.urls import reverse

Tags = (
    ('F', 'Fashion'),
    ('A', 'Art'),
    ('N', 'Nature'),
    ('E', 'Eats'),
    ('M', 'Music'),
    ('S', 'Sports'),
    ('P', 'Pets')
)
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'post_id': self.id})

class Category(models.Model):
        tag = models.CharField(max_length=1,
            choices=Tags,
            default=Tags[0][0]
        )
        post = models.ForeignKey(Post, on_delete=models.CASCADE)

        def __str__(self):
            return f'{self.get_tag_display()} for {self.post.title}'