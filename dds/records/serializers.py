from rest_framework import serializers

from records.models import Type, Status, Category, Subcategory


class RecordsSerializer(serializers.Serializer):
    id = serializers.IntegerField(source="pk", read_only=True)
    date =  serializers.DateField(read_only=True)
    status = serializers.CharField()
    type = serializers.CharField()
    category = serializers.CharField()
    subcategory = serializers.CharField()
    amount = serializers.IntegerField(min_value=1)
    comment = serializers.CharField(required=False, allow_blank=True)


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'
