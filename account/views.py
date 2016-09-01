# Create your views here.
#coding:utf8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import datetime
import sys,json
import psutil

from account.models import *
from system.views import save_log

reload(sys)
sys.setdefaultencoding('utf8')

def index(request):
	return render(request,'account/login.html')

@csrf_exempt
def account_login(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = auth.authenticate(username=username,password=password)
		if user and user.is_active:
			auth.login(request,user)
			save_log(username,"登陆系统","登陆成功")
			return HttpResponseRedirect('/home/')
		else:
			return render(request,'account/login.html',{'login_err': '登陆失败,请确认后重新输入'})
	else:
		return render(request,'account/login.html')

def account_logout(request):
	save_log(request.user,"退出系统","成功")
	auth.logout(request)
	return render(request,"account/login.html")

@login_required()
def home(request):
	net = psutil.net_io_counters()
	bytes_sent = '{0:.2f} Mb'.format(net.bytes_recv / 1024 / 1024)
	bytes_rcvd = '{0:.2f} Mb'.format(net.bytes_sent / 1024 / 1024)
	#net_list = ['bytes_sent','bytes_rcvd']
	kwvars = {
		'user':request.user,
		'cpu':(psutil.cpu_times()),
		'men':psutil.virtual_memory(),
		'disk':psutil.disk_partitions(),
		'net_sent':bytes_sent,
		'net_rcvd':bytes_rcvd,
		'sys_user':psutil.users(),
	}
	return render(request,'index.html',kwvars)

@login_required()
def profile(request):
	kwvars = {
		'user':request.user,
	}
	return render(request,"account/profile.html",kwvars)

@login_required()
def seeting(request):
	username = request.GET.get('save')
	username = request.POST.get('user')
	password = request.POST.get('old_pass')
	new_pass1 = request.POST.get('new_pass1')
	new_pass2 = request.POST.get('new_pass2')
	if username:
		if new_pass1 == new_pass2:
			user = auth.authenticate(username=username,password=password)
			if user and user.is_active:
				newuser = User.objects.get(username=username)
				newuser.set_password(new_pass1)
				try:
					newuser.save()
					save_log(request.user,"修改密码","修改成功")
					return render(request,'account/login.html')
				except Exception,e:
					kwvars = {
						'user':request.user,
						'log':"修改失败！！！",
					}
					save_log(request.user,"修改密码","修改失败")
					return render(request,"account/change_pass.html",kwvars)
			else:
				kwvars = {
					'user':request.user,
					'log':"请输入正确的密码！！！",
				}
				return render(request,"account/change_pass.html",kwvars)
		else:				
			kwvars = {
				'user':request.user,
				'log':"两次输入的密码不一致",
			}
			return render(request,"account/change_pass.html",kwvars)
	else:
		kwvars = {
			'user':request.user,
			'log':"修改成功将会要求重新登陆！！！",
		}
		return render(request,"account/change_pass.html",kwvars)

@login_required()
def man(request):
	kwvars = {
		'user':request.user,
	}
	return render_to_response("help.html",kwvars)

