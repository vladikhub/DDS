from django.db import models
from django.urls import reverse




class Status(models.Model):
    """
    Класс-модель сущности Статус операции

    Имеет поля:
    title - название статуса
    """
    title = models.CharField(unique=True, verbose_name="Название")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name="Статус"
        verbose_name_plural = "Статусы"

class Type(models.Model):
    """
        Класс-модель сущности Тип операции

        Имеет поля:
        title - название типа операции
    """
    title = models.CharField(unique=True, verbose_name="Название")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name="Тип операции"
        verbose_name_plural = "Типы операций"

class Category(models.Model):
    """
        Класс-модель сущности Категория операции

        Имеет поля:
        title - название категории
        type - тип операции (внешний ключ: Type)
    """
    title = models.CharField(unique=True, verbose_name="Название")
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name="Категория"
        verbose_name_plural = "Категории"

class Subcategory(models.Model):
    """
        Класс-модель сущности Подкатегория операции

        Имеет поля:
        title - название подкатегория
        category - категория операции (внешний ключ: Category)
    """
    title = models.CharField(unique=True, verbose_name="Название")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name="Подкатегория"
        verbose_name_plural = "Подкатегории"

class Records(models.Model):
    """
        Класс-модель сущности Записи операции

        Имеет поля:
        date - дата операции
        status - статус операции (внешний ключ: Status)
        type - тип операции (внешний ключ: Type)
        category - тип операции (внешний ключ: Category)
        subcategory - тип операции (внешний ключ: Subcategory)
        amount - сумма операции в рублях
        comment - комментарий (не обязателен)

    """
    date = models.DateField(auto_now_add=True, verbose_name="Дата")
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name="Статус")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name="Тип операции")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, verbose_name="Подкатегория")
    amount = models.IntegerField(verbose_name="Сумма операции")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")

    def __str__(self):
        return f"{self.type} - {self.amount}р."

    def get_absolute_url(self):
        return reverse("records-detail", kwargs={'pk': self.pk})


    class Meta:
        verbose_name="История записей"
        verbose_name_plural = "Истории записей"



