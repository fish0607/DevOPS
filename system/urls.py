from django.conf.urls import include, url
from django.contrib import admin
from system import views

urlpatterns = [
	url(r'^base/$',views.system_base),
	url(r'^soft/$',views.system_soft),
	url(r'^reboot/$',views.system_reboot),
	url(r'^check/$',views.system_check),
	url(r'^monitor/$',views.system_monitor),
	url(r'^shell/$',views.system_shell),
	url(r'^mail/$',views.system_mail),
	url(r'^logs/$',views.system_logs),
]
     
