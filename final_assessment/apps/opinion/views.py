from django.views.generic.edit import FormView, UpdateView
from django.views.generic.list import ListView
from apps.opinion.models import Opinions
from apps.opinion.forms import Opinion
from django.http.response import HttpResponse
from django.shortcuts import render
from apps.auction.models import Auction
from datetime import datetime

# Create your views here.

class Opinion_View(FormView):
    model = Auction
    form_class = Opinion
    template_name = 'opinion/opinion.html'

class AllOpinions(ListView):
    model = Auction
    template_name = 'opinion/all_opinions.html'
    context_object_name = 'auction'
    paginate_by = 3
 
    def get_queryset(self):
        today = datetime.now()
        queryset_date = Auction.objects.filter(ends__range=["1901-01-01", today], is_paid=True, creator_ID = self.request.user)
        queryset = Opinions.objects.filter(buyer_grade__isnull=False, auction_ID__creator_ID = self.request.user, auction_ID__ends__range=["1901-01-01", today], auction_ID__is_paid=True)
        return queryset