from django.core.exceptions import ValidationError

from records.models import Records
from records.selectors import get_status, get_type, get_subcategory, get_category

def create_record(data: dict):
    """
    Создает новую запись операции с валидацией зависимостей сущностей

    При несовпадении зависимостей выкидывает ошибку ValidationError

    Принимает:
        data: dict - словарь validated_data из сериализатора.
        В себе должен хранить:
            - status (str): Название статуса
            - type (str): Название типа операции
            - category (str): Название категории
            - subcategory (str): Название подкатегории
            - amount (int): Сумма операции
            - comment (str, optional): Комментарий к операции

    Возвращает:
        Records - созданный объект
    """
    status = get_status(data.get("status"))
    type = get_type(data.get("type"))
    category = get_category(data.get("category"))
    subcategory = get_subcategory(data.get("subcategory"))

    if category.type != type:
        raise ValidationError("Категория не принадлежит выбранному типу операции")

    if subcategory.category != category:
        raise ValidationError("Подкатегория не принадлежит выбранной категории")


    return Records.objects.create(
        status=status,
        type=type,
        category=category,
        subcategory=subcategory,
        amount=data["amount"],
        comment=data["comment"]
    )

def update_record(instance: Records, data: dict):
    """
    Обновляет существующую запись операции с валидацией зависимостей сущностей

    При несовпадении зависимостей выкидывает ошибку ValidationError

    Принимает:
        instance (Records): Объект записи, который нужно обновить
        data: dict - словарь validated_data из сериализатора.
        В себе должен хранить:
            - status (str): Название статуса
            - type (str): Название типа операции
            - category (str): Название категории
            - subcategory (str): Название подкатегории
            - amount (int): Сумма операции
            - comment (str, optional): Комментарий к операции

    Возвращает:
        Records - созданный объект
    """
    status = get_status(data.get("status", instance.status))
    type = get_type(data.get("type", instance.type))
    category = get_category(data.get("category", instance.category))
    subcategory = get_subcategory(data.get("subcategory", instance.subcategory))

    if category.type != type:
        raise ValidationError("Категория не принадлежит выбранному типу операции")

    if subcategory.category != category:
        raise ValidationError("Подкатегория не принадлежит выбранной категории")

    instance.status = status
    instance.type = type
    instance.category = category
    instance.subcategory = subcategory
    instance.amount = data.get("amount", instance.amount)
    instance.comment = data.get("comment", instance.comment)
    instance.save()
    return instance

def delete_record(instance: Records):
    """
    Удаляет существующую запись операции

    Принимает:
        instance (Records): Объект записи, который нужно обновить
    Возвращает:
        dict
    """
    instance.delete()
    return {"status": "OK"}