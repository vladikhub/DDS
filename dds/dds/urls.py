"""
URL configuration for dds project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers

from records.views import (ReadCreateRecordsAPIView,
                           RetrieveDetailRecordAPIView,
                           TypeViewSet, StatusViewSet,
                           CategoryViewSet, SubcategoryViewSet)

router = routers.SimpleRouter()
router.register("type", TypeViewSet)
router.register("status", StatusViewSet)
router.register("category", CategoryViewSet)
router.register("subcategory", SubcategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/records/', ReadCreateRecordsAPIView.as_view()),
    path('api/v1/records/<int:pk>/', RetrieveDetailRecordAPIView.as_view(), name='records-detail'),
    path('api/v1/', include(router.urls)),
    path('admin-api/categories/', CategoryViewSet.as_view({'get': 'for_admin'})),
    path('admin-api/subcategories/', SubcategoryViewSet.as_view({'get': 'for_admin'})),
]
