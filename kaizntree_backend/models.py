from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Item(models.Model):
    sku = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    stock_status = models.DecimalField(max_digits=10, decimal_places=3)
    available_stock = models.DecimalField(max_digits=10, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the field to now when the object is first created.
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set the field to now every time the object is saved.

    def __str__(self):
        return self.name
