# Create your views here.
#coding:utf8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import datetime
import sys,json
import string

from cmdb.models import *
from system.views import save_log

reload(sys)
sys.setdefaultencoding('utf8')

@login_required()
def cmdb_info(request):
	server_list = host_info.objects.all()
	change = request.GET.get('change')
	remove = request.GET.get('remove')
	save = request.GET.get('save')
	
	if change:
		server_info = host_info.objects.get(ip=change)
		kwvars = {
			'user':request.user,
			'info':server_info,
			'change':change,
		}
		return render_to_response('cmdb/host_change.html',kwvars)
	elif save:
		ip = request.GET.get('save')
		info = host_info.objects.get(ip=ip)
		info.hostname = request.POST.get('hostname')
		info.cpu = request.POST.get('cpu')
		info.men = request.POST.get('men')
		info.disk = request.POST.get('disk')
		info.os = request.POST.get('os')
		info.position = request.POST.get('position')
		info.owner = request.POST.get('owner')
		info.group = request.POST.get('group')
		info.notes = request.POST.get('notes')
		try:
			info.save()
			save_log(request.user,"修改主机信息：" + ip ,"修改成功")
			return HttpResponseRedirect('/cmdb/info/')
		except Exception,e:
			kwvars = {
				'user':request.user,
				'log':'Host info save fail...',
			}
			save_log(request.user,"修改主机信息：" + ip ,e)
			return render_to_response('cmdb/host_change.html',kwvars)	
	elif remove:
		del_host = host_info.objects.filter(ip=remove)
		del_ssh = ssh_info.objects.filter(ip=remove)
		del_host.delete()
		del_ssh.delete()
		save_log(request.user,"删除主机信息：" + ip ,"删除成功")
		return HttpResponseRedirect('/cmdb/info/')
	else:
		kwvars = {
			'user':request.user,
			'server_list':server_list,
		}
		return render_to_response('cmdb/host_info.html',kwvars)

@login_required()
def cmdb_ssh(request):
	ssh_list = ssh_info.objects.all()
	change = request.GET.get('change')
	remove = request.GET.get('remove')
	save = request.GET.get('save')
	kwvars = {
		'user':request.user,
		'ssh_list':ssh_list,
	}
	if change:
		ssh_list = ssh_info.objects.get(ip=change)
		kwvars = {
			'user':request.user,
			'info':ssh_list,
			'change':change,
		}
		return render_to_response('cmdb/ssh_change.html',kwvars)
	elif save:
		ip = request.GET.get('save')
		info = ssh_info.objects.get(ip=ip)
		info.hostname = request.POST.get('hostname')
		info.ip = request.POST.get('ip')
		info.username = request.POST.get('username')
		info.password = request.POST.get('password')
		info.port = request.POST.get('port')
		info.notes = request.POST.get('notes')
		try:
			info.save()
			save_log(request.user,"修改主机SSH信息：" + ip ,"修改成功")
			return HttpResponseRedirect('/cmdb/ssh/')
		except Exception,e:
			kwvars = {
				'user':request.user,
				'log':'SSH info save fail...',
			}
			save_log(request.user,"修改主机SSH信息：" + ip ,"修改失败")
			return render_to_response('cmdb/ssh_change.html',kwvars)
	elif remove:
		del_host = host_info.objects.filter(ip=remove)
		del_ssh = ssh_info.objects.filter(ip=remove)
		del_host.delete()
		del_ssh.delete()
		save_log(request.user,"删除主机：" + remove ,"删除成功")
		return HttpResponseRedirect('/cmdb/ssh/')
	return render_to_response('cmdb/ssh_info.html',kwvars)

@login_required()	
def cmdb_add(request):
	ip = request.POST.get('ip')
	if ip is None:
		kwvars = {
			'user':request.user,
			'log':"注意： IP 不能为空！！！",
		}
		return render_to_response('cmdb/host_add.html',kwvars)
	else:
		hostname = request.POST.get('hostname')
		cpu = request.POST.get('cpu')
		men = request.POST.get('men')
		disk = request.POST.get('disk')
		os = request.POST.get('os')
		position = request.POST.get('position')
		owner = request.POST.get('owner')
		group = request.POST.get('group')
		notes = request.POST.get('notes')
		host_sql = host_info(hostname=hostname,ip=ip,cpu=cpu,men=men,disk=disk,os=os,position=position,owner=owner,group=group,notes=notes)
		ssh_sql = ssh_info(hostname=hostname,ip=ip,username='',password='',port='',notes=notes)
		try:
			host_sql.save()
			ssh_sql.save()
			server_list = host_info.objects.all()
			kwvars = {
				'user':request.user,
				'server_list':server_list,
			}		
			save_log(request.user,"添加主机信息：" + ip ,"添加成功")	
			return render_to_response('cmdb/host_info.html',kwvars)
		except Exception,e:
			kwvars = {
				'user':request.user,
				'log':e,
			}
			save_log(request.user,"添加主机信息：" + ip ,e) 
			return render_to_response('cmdb/host_add.html',kwvars)

