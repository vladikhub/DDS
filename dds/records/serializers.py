from rest_framework import serializers

from records.models import Type, Status, Category, Subcategory


class RecordsSerializer(serializers.Serializer):
    """
    Сериализатор для записей операций

    Поля:
        id (int, read-only): Уникальный идентификатор записи (первичный ключ).
        date (date, read-only): Дата операции.
        status (str): Статус операции.
        type (str): Тип операции.
        category (str): Категория операции.
        subcategory (str): Подкатегория операции.
        amount (int): Сумма операции (должна быть положительной).
        comment (str, optional): Дополнительный комментарий к операции.
    """
    id = serializers.IntegerField(source="pk", read_only=True)
    date =  serializers.DateField(read_only=True)
    status = serializers.CharField()
    type = serializers.CharField()
    category = serializers.CharField()
    subcategory = serializers.CharField()
    amount = serializers.IntegerField(min_value=1)
    comment = serializers.CharField(required=False, allow_blank=True)


class StatusSerializer(serializers.ModelSerializer):
    """
    Сериализатор на основе модели Status
    """
    class Meta:
        model = Status
        fields = '__all__'


class TypeSerializer(serializers.ModelSerializer):
    """
        Сериализатор на основе модели Type
    """
    class Meta:
        model = Type
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """
        Сериализатор на основе модели Category
    """
    class Meta:
        model = Category
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    """
        Сериализатор на основе модели Subcategory
    """
    class Meta:
        model = Subcategory
        fields = '__all__'
