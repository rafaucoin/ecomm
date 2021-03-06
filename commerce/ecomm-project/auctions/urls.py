from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.createListing, name="create-listing"),
    path("listing/<str:pk>", views.listing, name="listing"),   
    path("watchlist", views.watchlist, name="watchlist"),

]
