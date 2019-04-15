from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Users(models.Model):
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=20)

    def __str__(self):
        return str(self.email)


class Products(models.Model):
    name = models.CharField(max_length=100)
    nutriscore = models.CharField(max_length=1)
    category = ArrayField(models.CharField(max_length=900, default='{}'), blank=True, size=None, default=list, null=True)
    picture = models.URLField()
    url = models.URLField()

    def __str__(self):
        return self.name


class Saving(models.Model):
    contact = models.CharField(max_length=100, default='')
    product_key = models.CharField(max_length=9000, default='')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.contact)

    class Meta:
        ordering = ['date']
