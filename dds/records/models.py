from django.db import models


class Status(models.Model):
    title = models.CharField(unique=True)

    def __str__(self):
        return self.title

class Type(models.Model):
    title = models.CharField(unique=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    title = models.CharField(unique=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Subcategory(models.Model):
    title = models.CharField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Records(models.Model):
    date = models.DateField(auto_now_add=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    amount = models.IntegerField()
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.type} - {self.amount}р."



