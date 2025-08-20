# models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    image = models.ImageField(upload_to='books/')
    source_type = models.IntegerField(
        choices=[(1, 'FBV'), (2, 'CBV')],
        default=1
    )
