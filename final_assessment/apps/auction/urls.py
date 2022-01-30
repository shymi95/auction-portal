from django.urls import path
from apps.auction import views

app_name = 'auction'

urlpatterns = [
    path('searchbox/', views.Searchbox.as_view(), name='searchbox'),
    path('auction/<int:pk>', views.Auction_View.as_view(), name='auction'),
    path('auction/create', views.CreateAuction.as_view(), name='create_view'),
    path('searchbox/<str:category>', views.CategoryResults.as_view(), name='searchbox_category'),
    path('auction/<int:pk>/follow', views.FollowAuction.as_view(), name='follow_auction'),
    path('auction/followed', views.Followed.as_view(), name='followed'),

]