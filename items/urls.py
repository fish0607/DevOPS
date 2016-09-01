from django.conf.urls import include, url
from django.contrib import admin
from items import views

urlpatterns = [
	url(r'^info/$',views.items_info_echo,name='items_info'),
	url(r'^add/$',views.items_add,name='items_add'),
	url(r'^monitor/$',views.items_monitor),
	url(r'^logs/$',views.items_logs),
]
