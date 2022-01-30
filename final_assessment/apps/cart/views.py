from apps.opinion.models import Opinions
from apps.opinion.forms import Opinion
from apps.cart.forms import Address
from apps.auction.forms import AuctionUpdate
from datetime import datetime
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin, FormView, UpdateView
from apps.auction.models import Auction, FollowedAuctions
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.urls import reverse

# Create your views here.

class Cart(ListView):
    model = Auction
    template_name = 'cart/cart.html'
    context_object_name = 'auction'
    paginate_by = 3
 
    def get_queryset(self):
        today = datetime.now()
        queryset_date = Auction.objects.filter(ends__range=["1901-01-01", today], is_paid=False)
        result = queryset_date.filter(buyer_ID = self.request.user)
        return result

class Item(DetailView, FormMixin):
    template_name = 'cart/item.html'
    model = Auction
    form_class = Opinion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['graded'] = Opinions.objects.filter(auction_ID__id = self.kwargs['pk']).exists()
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def form_valid(self, form):
        # auction = Auction.objects.filter(id=self.kwargs['pk']
        # buyer_grade = form.cleaned_data.get('buyer_grade')
        # buyer_comment = form.cleanded_data.get('buyer_comment')
        form.instance.auction_ID = Auction.objects.filter(id=self.kwargs['pk']).first()
        form.instance.commentator_ID = self.request.user
        # opinion = Opinions(auction_ID=Auction.objects.filter(id=self.kwargs['pk']), commentator_ID=self.request.user, buyer_grade=buyer_grade, buyer_comment=buyer_comment)
        form.instance.save()
        return self.render_to_response({
            'auction': Auction.objects.filter(id=self.kwargs['pk']).first(),
            'graded': Opinions.objects.filter(auction_ID__id = self.kwargs['pk']).exists()
        })

class Finalize(FormView):
    model = Auction
    template_name = 'cart/finalize.html'
    form_class = Address

    def form_valid(self, pk):
        update_auction = Auction.objects.get(id=self.kwargs['pk'])
        update_auction.is_paid = True
        update_auction.save()
        return redirect(reverse('cart:item', args=(update_auction.id,)))

class Purchased(ListView):
    model = Auction
    template_name = 'cart/cart.html'
    context_object_name = 'auction'
    paginate_by = 3
 
    def get_queryset(self):
        today = datetime.now()
        queryset_date = Auction.objects.filter(ends__range=["1901-01-01", today], is_paid=True)
        result = queryset_date.filter(buyer_ID = self.request.user)
        return result





 
