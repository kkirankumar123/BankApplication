from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('Bhome',views.Bhome),
    path('Ahome',views.Ahome),
    path('openAC',views.openAC),
    path('withdraw',views.withdraw),
    path('deposit',views.deposite),
    path('balanceEnq',views.balanceEnq),
    path('changeMobile',views.changeMobile),
    path('fundTransfer',views.fundTransfer),
    path('closeAC',views.closeAC),
    path('transaction',views.transaction),

]

