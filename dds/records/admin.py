from django.contrib import admin
from rangefilter.filters import DateRangeFilter

from records.forms import RecordForm
from records.models import Status, Type, Category, Subcategory, Records


# Register your models here.

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type')


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category')


@admin.register(Records)
class RecordsAdmin(admin.ModelAdmin):
    form = RecordForm
    list_display = ( 'date', 'status',
                    'type', 'category', 'subcategory',
                    'amount', 'comment')

    list_filter = ('status', 'type', 'category', 'subcategory', ('date', DateRangeFilter))
    ordering = ('-date',)
