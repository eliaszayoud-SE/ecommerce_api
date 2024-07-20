from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category/images')
    date = models.DateField(auto_now_add=True)


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    description_ar = models.CharField(max_length=255)
    image = models.ImageField(upload_to='items/image')
    count = models.IntegerField()
    active = models.BooleanField(default=True)
    price = models.FloatField()
    discount = models.SmallIntegerField()
    date = models.DateField(auto_now_add=True)