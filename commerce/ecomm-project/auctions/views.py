from multiprocessing import context
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing, Watchlist, Bid, Comment
from .forms import ListingForm
from django.contrib.auth.decorators import login_required


def index(request):
    listing = Listing.objects.all()
    Listings = listing
    context = {'Listings': Listings}
    return render(request, "auctions/index.html", {'Listings': Listings})


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def createListing(request):
    res = Listing()
    form = ListingForm()
    context = {'form': form}
    if request.method == "POST":
        res.price = request.POST['price']
        listings = Listing.objects.filter(
            title=request.POST['title'], host=request.user)
        if len(listings) > 0:
            return render(request, "auctions/create-listing.html", {'exist': True})
        res.title = request.POST['title']

        res.desc = request.POST['description']
        res.image = request.POST['image']
        res.host = request.user
        res.category = request.POST['category']
        bid = Bid()
        bid.user = res.host
        bid.price = res.price
        bid.title = res.title
        bid.save()
        res.bid = bid
        res.save()
        return redirect('index')
    return render(request, "auctions/create-listing.html", context)


def listing(request, pk):
    listing = Listing.objects.get(id=pk)
    comments = Comment.objects.filter(listing=listing)
    if request.user.is_authenticated == False:
        return render(request, "auctions/listing.html", {'item': listing, 'creator': False})
    element = Watchlist.objects.filter(user=request.user, listing=listing)
    if request.method == "POST" and 'comment' in request.POST:
        comment = Comment()
        comment.user = request.user
        comment.listing = listing
        comment.body = request.POST['body']
        comment.save()
    if request.user == listing.host:
        if request.method == "POST" and 'close' in request.POST:
            listing.active = False
            listing.save()
            return render(request, "auctions/listing.html", {'item': listing, 'creator': True, 'comments': comments})

        if request.method == "POST" and 'open' in request.POST:
            listing.active = True
            listing.save()
            return render(request, "auctions/listing.html", {'item': listing, 'creator': True, 'comments': comments})

        return render(request, "auctions/listing.html", {'item': listing, 'creator': True, 'comments': comments})
    exist = False
    try:
        if request.method == "POST" and 'btnform1' in request.POST and (element[0] not in Watchlist.objects.all()):
            exist = False
            Watchlist.objects.create(user=request.user, listing=listing)
        if request.method == "POST" and 'btnform1' in request.POST and (element[0] in Watchlist.objects.all()):
            exit = True
            element[0].delete()
    except IndexError:
        if request.method == "POST" and 'btnform1' in request.POST and (element not in Watchlist.objects.all()):
            Watchlist.objects.create(user=request.user, listing=listing)
            exist = True
        if request.method == "POST" and 'btnform1' in request.POST and (element in Watchlist.objects.all()):
            exit = True
            element.delete()
    if request.method == "POST" and 'btnform2' in request.POST:
        price = request.POST['bid']

        # bid.save()
        if int(price) > listing.bid.price:
            bid = Bid()
            bid.user = request.user
            bid.price = price
            bid.title = listing.title
            bid.save()
            listing.bid = bid
            listing.save()
            current = listing.bid.price
    current = listing.bid.price
    return render(request, "auctions/listing.html", {'item': listing, 'exist': exist, 'creator': False, 'comments': comments})


def watchlist(request):
    collection = Watchlist.objects.filter(user=request.user)

    return render(request, "auctions/watchlist.html", {'collection': collection})
