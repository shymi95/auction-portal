from django.urls import path
from apps.main import views

app_name = 'main'

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('categories', views.Categories.as_view(), name="categories"),
    path('categories/category', views.Categories, name="category"),
]