from django.db.models.deletion import CASCADE
from apps.main.models import Categories
from apps.user_handler.models import CustomUser
from django.db import models

# Create your models here.


class Auction(models.Model):
    creator_ID = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='creator')
    buyer_ID = models.ForeignKey(CustomUser, default="", null=True, on_delete=models.CASCADE, related_name='buyer')
    category_ID = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    ends = models.DateTimeField()
    is_paid = models.BooleanField(default=False)
    minimal_price = models.FloatField()
    current_price = models.FloatField(default=0, verbose_name='Twoja cena:')

    def __str__(self):
        return self.title
    

class FollowedAuctions(models.Model):
    user_ID = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    auction_ID = models.ForeignKey(Auction, on_delete=models.CASCADE)


class Record(models.Model):
    auction_ID = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidder_ID = models.ForeignKey(CustomUser,blank=True, default="", on_delete=models.CASCADE)
    price = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)