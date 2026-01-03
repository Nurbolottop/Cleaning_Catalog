from django.urls import path
from apps.base import views as base_viwes
urlpatterns = [
    path('', base_viwes.index, name = "index-page")
]
