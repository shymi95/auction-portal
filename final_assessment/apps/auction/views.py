from django.views.generic.list import MultipleObjectMixin
from apps.main.models import Categories
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormMixin, FormView, UpdateView
from .forms import AuctionForm, AuctionUpdate, Searchbox
from apps.auction.models import Auction
from apps.auction.models import Auction, FollowedAuctions, Record
from django.views.generic import ListView
from django.views.generic.base import View
from datetime import datetime  
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class Auction_View(UpdateView):
    model = Auction
    template_name = 'auction/auction.html'
    update_successful = None
    form_class = AuctionUpdate
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        if FollowedAuctions.objects.all().filter(user_ID = self.request.user, auction_ID_id = self.kwargs['pk']).exists():
            context['follow'] = 'Odśledź'
        else:
            context['follow'] = 'Śledź'
        return context
 
    def form_valid(self, form, **kwargs):
        if form.is_valid():
            update_price = form.cleaned_data.get('current_price')
            update_auction = Auction.objects.get(id=self.kwargs['pk'])
            context = self.get_context_data()
 
            if update_price > update_auction.current_price:         
                self.db_updates(update_price, update_auction)
                context['update_successful'] = True
                context['bidder'] = Auction.objects.get(id=self.kwargs['pk']).buyer_ID
                context['display_price'] = Auction.objects.get(id=self.kwargs['pk']).current_price
                return self.render_to_response(context)
            else:
                context['update_successful'] = False
                context['display_price'] = Auction.objects.get(id=self.kwargs['pk']).current_price
                return self.render_to_response(context)
 
    def db_updates(self, update_price, update_auction):
        current_user = self.request.user
        update_auction.current_price = update_price
        update_auction.buyer_ID = current_user
        update_auction.save()
        update_record = Record(auction_ID = update_auction, bidder_ID = current_user, price=update_price)
        update_record.save()
        if not FollowedAuctions.objects.all().filter(user_ID = current_user, auction_ID = update_auction).exists():
            update_follow = FollowedAuctions(user_ID = current_user, auction_ID = update_auction)
            update_follow.save()
 
class Searchbox(ListView, FormMixin):
    model = Auction
    template_name = 'auction/searchbox.html'
    paginate_by = 3
    form_class = Searchbox
 
    def get_queryset(self):
        today = datetime.now()
        queryset = Auction.objects.all().filter(ends__range=[today, "9999-01-01"])
        return queryset

    def post(self, request):
        form = self.get_form()
        return render(self.request, 'auction/searchbox.html', self.get_custom_context_data(form))

    def get_custom_context_data(self, form, **kwargs):
        if form.is_valid():
            result = form.cleaned_data.get("search_key")
            today = datetime.now()
            initial_queryset = Auction.objects.filter(ends__range=[today, "9999-01-01"], is_paid=False)
            result = initial_queryset.filter(
            Q(title__icontains=result) | Q(current_price__icontains=result) | Q(description__icontains=result)
                )
        return {
        'form': self.get_form(),  
        'object_list': result,
            }   
 
class CreateAuction(CreateView):
    template_name = 'auction/create.html'
    form_class = AuctionForm
 
    def form_valid(self, form):
        form.instance.creator_ID = self.request.user
        form.instance.current_price = form.instance.minimal_price
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('auction:auction', args=(self.object.id,))
 
class FollowAuction(View):
    def post(self, request, pk, *args, **kwargs):
        try: 
            followed_auction = FollowedAuctions.objects.get(user_ID = self.request.user, auction_ID = Auction.objects.get(id=pk))
        except:
            followed_auction = FollowedAuctions(user_ID = self.request.user, auction_ID = Auction.objects.get(id=pk))
            followed_auction.save()
        else:
            followed_auction.delete()
        return redirect(reverse('auction:auction', args=(pk, )))
 
class Followed(ListView):
    model = FollowedAuctions
    template_name = 'auction/followed.html'
    context_object_name = 'auction'
    paginate_by = 3
 
    def get_queryset(self):
        today = datetime.now()
        queryset_date = Auction.objects.filter(ends__range=[today, "9999-01-01"], is_paid=False)
        queryset = queryset_date.filter(followedauctions__user_ID=self.request.user)
        return queryset

class CategoryResults(ListView):
    model = Auction
    template_name = 'auction/category_results.html'
    context_object_name = 'auction'
    paginate_by = 3

    def get_queryset(self):
        today = datetime.now()
        queryset_date = Auction.objects.filter(ends__range=[today, "9999-01-01"], is_paid=False)
        category = Categories.objects.get(category=self.kwargs['category'])
        result = queryset_date.filter(category_ID=category.id)
        return result
 


 
 
 

