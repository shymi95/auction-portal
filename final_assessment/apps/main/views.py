from apps.auction.models import Auction
from django.db.models import Sum
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from .models import Categories

# Create your views here.

class Index(TemplateView):
    template_name = 'main/index.html'

class Categories(ListView):
    model = Categories
    context_object_name = 'object_list'
    template_name = 'main/categories.html'

    def post(request):
        print("request")