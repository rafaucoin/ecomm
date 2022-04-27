from re import L
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField(max_length=9999999999)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, null=False, default='')

    def __str__(self):
        return str(self.title)


class Listing(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    bid = models.ForeignKey(Bid, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=70)
    description = models.TextField()
    image = models.CharField(max_length=255, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Category(models.TextChoices):
        first = "firstCat"
        second = "secondCat"
        third = "thirdCat"
        fourth = "fourthCat"

    category = models.CharField(
        max_length=15,
        choices=Category.choices,
        default=Category.first
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    body = models.TextField()


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username + str(self.listing.id)
