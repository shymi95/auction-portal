from apps.user_handler.models import CustomUser
from apps.auction.models import Auction
from django.db import models

# Create your models here.

class Opinions(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    auction_ID = models.ForeignKey(Auction, on_delete=models.CASCADE)
    commentator_ID = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    buyer_grade = models.IntegerField(choices=RATING_CHOICES)
    buyer_comment = models.CharField(max_length=250)
    pub_date = models.DateTimeField(auto_now_add=True)