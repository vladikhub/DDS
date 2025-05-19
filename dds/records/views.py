import datetime

from django.core.exceptions import ValidationError
from django.shortcuts import render
from rest_framework.decorators import action

from rest_framework.response import Response
from rest_framework import viewsets, views
from rest_framework.views import APIView
from unicodedata import category

from records.models import Records, Type, Status, Category, Subcategory
from records.serializers import RecordsSerializer, TypeSerializer, StatusSerializer, CategorySerializer, \
    SubcategorySerializer
from records.selectors import get_record_by_id, get_filtered_records
from records.services import create_record, update_record, delete_record


class ReadCreateRecordsAPIView(views.APIView):
    """
        API endpoint для получения и создания записей операций.
        /api/v1/records/
        Поддерживает:
        - GET: Получение отфильтрованного списка записей
        - POST: Создание новой записи
    """
    def get(self, request):
        """
            Возвращает отфильтрованный список финансовых записей.

            Параметры запроса (query parameters):
                date_from (date, optional): Начальная дата периода
                date_to (date, optional): Конечная дата периода. По умолчанию: сегодня
                status (str, optional): Фильтр по статусу записи
                type (str, optional): Фильтр по типу операции
                category (str, optional): Фильтр по категории
                subcategory (str, optional): Фильтр по подкатегории
            """
        query = get_filtered_records(
            date_from=request.query_params.get("date_from"),
            date_to=request.query_params.get("date_to", datetime.date.today()),
            status=request.query_params.get("status"),
            type=request.query_params.get("type"),
            category=request.query_params.get("category"),
            subcategory=request.query_params.get("subcategory"),
        )
        return Response({'records': RecordsSerializer(query, many=True).data})

    def post(self, request):
        """
            Создает новую запись операции.

            Тело запроса (JSON):
                {
                    "status": "Бизнес",    # обязательное
                    "type": "Списание",        # обязательное
                    "category": "Маркетинг",       # обязательное
                    "subcategory": "Avito", # обязательное
                    "amount": 1500,          # обязательное, > 0
                    "comment": ""        # необязательное
                }

            Возвращает:
            Response: {
                "record": {
                    "id": 1,
                    "date": "2023-01-15",
                    ...
                }
            }
        """
        serializer = RecordsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            new_record = create_record(serializer.validated_data)
        except ValidationError as e:
            return Response({'error': e.message}, status=400)

        return Response({'record': RecordsSerializer(new_record).data})


class RetrieveDetailRecordAPIView(views.APIView):
    """
    API endpoint для получения, обновления, удаления записей операций
    Доступные методы:
    /api/v1/records/<int:pk>/
    GET - получение записи по ключу
    PUT - полное обновление
    PATCH - частичное обновление
    DELETE - удаление записи
    """
    def get(self, request, *args, **kwargs):
        """
        Получение конкретной записи по ключу

        Возвращает:
            Response: {
                "record": {
                    "id": 42,
                    "date": "2023-01-15",
                    ...
                }
            }
        """
        pk = kwargs.get("pk", None)
        if pk:
            try:
                query = get_record_by_id(pk)
            except ValidationError as e:
                return Response({'error': e.message})
            return Response({'record': RecordsSerializer(query).data})

    def put(self, request, partial=False, *args, **kwargs):
        """
        Полностью обновляет запись операции.

        Принимает pk объекта, если такого объекта не существует, выкидывает исключение

        Требует всех полей записи

        Возвращает:
            Response: {
                "record": {
                    "id": 42,
                    ... (обновленные данные)
                }
            }
        """
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT is not allowed"})
        try:
            instance = get_record_by_id(pk)
        except ValidationError as e:
            return Response({'error': e.message}, status=400)

        serializer = RecordsSerializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            record = update_record(instance, serializer.validated_data)
        except ValidationError as e:
            return Response({'error': e.message}, status=400)
        return Response({'record': RecordsSerializer(record).data})

    def patch(self, request, *args, **kwargs):
        """
        Частично обновляет запись операции

        Вызывает метод put(), но со значением partial=True
        """
        return self.put(request, True, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Удаляет запись операции

        Если запись не найдена, выкидывает исключение
        """
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT is not allowed"})
        try:
            instance = get_record_by_id(pk)
        except ValidationError as e:
            return Response({'error': e.message}, status=400)
        res = delete_record(instance)
        return Response(res)



class TypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Type (операции CRUD)
    """
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class StatusViewSet(viewsets.ModelViewSet):
    """
        ViewSet для модели Status (операции CRUD)
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
        ViewSet для модели Category (операции CRUD)

        Дополнительный экшн:
            for_admin() - ручка для админ-понели,
            получение категории по типу операции
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, url_path='for-admin')
    def for_admin(self, request):
        """

        Получает категории по типу операции
        """
        type_id = request.GET.get('type_id')
        categories = self.queryset.filter(type_id=type_id)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)


class SubcategoryViewSet(viewsets.ModelViewSet):
    """
        ViewSet для модели Subcategory (операции CRUD)

        Дополнительный экшн:
            for_admin() - ручка для админ-понели,
            получение подкатегории по категории операции
    """
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

    @action(detail=False, url_path='for-admin')
    def for_admin(self, request):
        """

        Получает подкатегории по категории
        """
        category_id = request.GET.get('category_id')
        subcategories = self.queryset.filter(category_id=category_id)
        serializer = self.get_serializer(subcategories, many=True)
        return Response(serializer.data)

