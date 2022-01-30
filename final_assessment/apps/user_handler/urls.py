from django.urls import path
from apps.user_handler import views

app_name = 'user_handler'

urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('registration', views.Registration.as_view(), name='registration'),
    path('logout', views.Logout.as_view(), name='logout')
]