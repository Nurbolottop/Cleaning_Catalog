from django.urls import path
from apps.cms import views as cms_views
urlpatterns = [
    path('category/', cms_views.category, name = "category-page"),
    path('category/<int:pk>/', cms_views.category_detail, name="category-detail"),
    path('service/<slug:slug>/', cms_views.service_detail, name="service-detail"),
]
