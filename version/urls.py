from django.conf.urls import include, url
from django.contrib import admin
from version import views

urlpatterns = [
	url(r'^info/$',views.versioning_show,name='show_version'),
	url(r'^add/$',views.versioning_add,name='add_version'),
]
