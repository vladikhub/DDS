import datetime

from django.core.exceptions import ValidationError
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import viewsets, views

from records.models import Records, Type, Status, Category, Subcategory
from records.serializers import RecordsSerializer, TypeSerializer, StatusSerializer, CategorySerializer, \
    SubcategorySerializer
from records.selectors import get_record_by_id, get_filtered_records
from records.services import create_record, update_record, delete_record


class ReadCreateRecordsAPIView(views.APIView):
    def get(self, request):
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
        serializer = RecordsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            new_record = create_record(serializer.validated_data)
        except ValidationError as e:
            return Response({'error': e.message}, status=400)

        return Response({'record': RecordsSerializer(new_record).data})


class RetrieveDetailRecordAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk:
            try:
                query = get_record_by_id(pk)
            except ValidationError as e:
                return Response({'error': e.message})
            return Response({'record': RecordsSerializer(query).data})

    def put(self, request, partial=False, *args, **kwargs):
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
        return self.put(request, True, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
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
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

