import datetime

from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.db.models.sql import Query
from rest_framework.generics import get_object_or_404

from records.models import Records, Status, Type, Category, Subcategory

def get_filtered_records(
        date_from=None,
        date_to=datetime.date.today(),
        status=None,
        type=None,
        category=None,
        subcategory=None
) -> QuerySet[Records]:
    """
    Возвращает отфильтрованный QuerySet записей по параметрам

    Принимает:
        date_from (date, optional)
            Если не указана, фильтрация будет по условию (<= date_to).
        date_to (date)
            По умолчанию - текущая дата.
        status (str, optional): Фильтр по названию статуса.
        type (str, optional): Фильтр по названию типа.
        category (str, optional): Фильтр по названию категории.
        subcategory (str, optional): Фильтр по названию подкатегории.

    Возвращает:
        QuerySet[Records]
    """
    query = Records.objects.all()
    if type:
        query = query.filter(type__title=type)
    if category:
        query = query.filter(category__title=category)
    if subcategory:
        query = query.filter(subcategory__title=subcategory)
    if status:
        query = query.filter(status__title=status)
    if date_from is None:
        query = query.filter(date__lte=date_to)
    else:
        query = query.filter(date__range=(date_from, date_to))
    return query


def get_record_by_id(pk: int) -> Records:
    """
    Возвращает запись по ID
    или выкидывает ошибку ValidationError, если значение не найдено

    Принимает:
        pk: int - первичный ключ

    Возвращает:
        Records
    """
    try:
        return Records.objects.get(pk=pk)
    except Records.DoesNotExist:
        raise ValidationError("Record does not exist")

def get_type(title: str) -> Type:
    """
        Возвращает тип операции по названию
        или выкидывает ошибку ValidationError, если значение не найдено

        Принимает:
            title: str - название типа операции

        Возвращает:
            Type
    """
    try:
        return Type.objects.get(title=title)
    except Type.DoesNotExist:
        raise ValidationError("Type does not exist")

def get_status(title: str) -> Status:
    """
        Возвращает статус операции по названию
        или выкидывает ошибку ValidationError, если значение не найдено

        Принимает:
            title: str - название статуса операции

        Возвращает:
            Status
    """
    try:
        return Status.objects.get(title=title)
    except Status.DoesNotExist:
        raise ValidationError("Status does not exist")

def get_category(title: str) -> Category:
    """
        Возвращает категорию операции по названию
        или выкидывает ошибку ValidationError, если значение не найдено

        Принимает:
            title: str - название категории операции

        Возвращает:
            Category
    """
    try:
        return Category.objects.get(title=title)
    except Category.DoesNotExist:
        raise ValidationError("Category does not exist")

def get_subcategory(title: str) -> Subcategory:
    """
        Возвращает подкатегорию операции по названию
        или выкидывает ошибку ValidationError, если значение не найдено

        Принимает:
            title: str - название подкатегории операции

        Возвращает:
            Subcategory
    """
    try:
        return Subcategory.objects.get(title=title)
    except Subcategory.DoesNotExist:
        raise ValidationError("Subcategory does not exist")

def get_category_by_type(type_id: int) -> Category:
    """
        Возвращает категорию операции по ID типа операции, так они зависимы
        или выкидывает ошибку ValidationError, если значение не найдено

        Принимает:
            type_id: int - ID типа операции

        Возвращает:
            Category
    """
    try:
        return Category.objects.get(type_id=type_id)
    except Category.DoesNotExist:
        raise ValidationError("Category does not exist")

def get_subcategory_by_category(category_id: int):
    """
            Возвращает подкатегорию операции по ID категории операции, так они зависимы
            или выкидывает ошибку ValidationError, если значение не найдено

            Принимает:
                category_id: int - ID категории операции

            Возвращает:
                Subcategory
        """
    try:
        return Subcategory.objects.get(category_id=category_id)
    except Subcategory.DoesNotExist:
        raise ValidationError("Subcategory does not exist")