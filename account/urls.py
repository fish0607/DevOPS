from django.conf.urls import include, url
from django.contrib import admin
from account import views

urlpatterns = [
	url(r'^login/$',views.account_login,name='login'),
    url(r'^logout/$',views.account_logout,name='logout'),
	url(r'^seeting/$',views.seeting,name='seeting'),
	url(r'^profile/$',views.profile,name='profile'),
]
