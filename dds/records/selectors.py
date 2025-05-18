import datetime

from django.core.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from records.models import Records, Status, Type, Category, Subcategory

def get_filtered_records(date_from=None, date_to=datetime.date.today(), status=None, type=None, category=None, subcategory=None):

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


def get_record_by_id(pk: int):
    try:
        return Records.objects.get(pk=pk)
    except Records.DoesNotExist:
        raise ValidationError("Record does not exist")

def get_type(title: str):
    try:
        return Type.objects.get(title=title)
    except Type.DoesNotExist:
        raise ValidationError("Type does not exist")

def get_status(title: str):
    try:
        return Status.objects.get(title=title)
    except Status.DoesNotExist:
        raise ValidationError("Status does not exist")

def get_category(title: str):
    try:
        return Category.objects.get(title=title)
    except Category.DoesNotExist:
        raise ValidationError("Category does not exist")

def get_subcategory(title: str):
    try:
        return Subcategory.objects.get(title=title)
    except Subcategory.DoesNotExist:
        raise ValidationError("Subcategory does not exist")