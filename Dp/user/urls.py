from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="UserHome"),
    path('about/', views.about, name="About"),
    path('contact/', views.contact, name="Contact"),
    path('search/', views.search, name="Search"),
    path('checkout/', views.checkout, name="Checkout"),
    path('products/<int:myid>', views.productView, name="ProductView"),
    path('handlerequest/', views.handlerequest, name="HandlerRequest"),
]