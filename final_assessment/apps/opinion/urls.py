from django.urls import path
from apps.opinion import views

app_name = 'opinion'

urlpatterns = [
    path('opinion/<int:pk>', views.Opinion_View.as_view(), name='opinion'),
    path('all-opinions', views.AllOpinions.as_view(), name='all_opinions'),
]