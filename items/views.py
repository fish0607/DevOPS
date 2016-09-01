# Create your views here.
#coding:utf8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
import sys

from items.models import *
from system.views import save_log

reload(sys)
sys.setdefaultencoding('utf8')

@login_required()
def items_info_echo(request):
	items_list = items_info.objects.all()
	edit_id = request.GET.get('edit')
	save_id = request.GET.get('save')
	start_id = request.GET.get('start')
	stop_id = request.GET.get('stop')
	restart_id = request.GET.get('restart')
	update_id = request.GET.get('update')
	remove_id = request.GET.get('remove')
	if edit_id:
		items_list = items_info.objects.get(items_id=edit_id)
		kwvars = {
			'user':request.user,
			'items':items_list,
		}
		return render_to_response("items/items_change.html",kwvars)
	elif save_id:
		info = items_info.objects.get(items_id=save_id)	
		info.host = request.POST.get('host')
		info.name = request.POST.get('name')
		info.service = request.POST.get('service')
		info.path = request.POST.get('path')
		info.shell = request.POST.get('shell')
		info.process = request.POST.get('process')
		info.port = request.POST.get('port')
		info.status = request.POST.get('status')
		info.group = request.POST.get('group')
		info.notes = request.POST.get('notes')
		try:
			info.save()
			save_log(request.user,"修改应用信息：" + info.name ,"修改成功")
			return HttpResponseRedirect('/items/info/')
		except Exception,e:
			kwvars = {
				'user':request.user,
				'items':items_list,
				'log':"应用信息修改失败",
			}
			save_log(request.user,"修改应用信息：" + info.name ,"修改失败")
			return render_to_response("items/info.html",kwvars)
	else:
		kwvars = {
			'user':request.user,
			'items_list':items_list,
		}
		return render_to_response("items/info.html",kwvars)

@login_required()
def items_add(request):
	host = request.POST.get('host')
	name = request.POST.get('name')
	service = request.POST.get('service')
	path = request.POST.get('path')
	shell = request.POST.get('shell')
	process = request.POST.get('process')
	port = request.POST.get('port')
	status = request.POST.get('status')
	group = request.POST.get('group')
	notes = request.POST.get('notes')
	not_null = [host,name,service,path,shell]
	for i in not_null:
		if i is None:
			kwvars = {
				'user':request.user,
				'log':'应用信息不完整，请填充完整',
			}
			return render_to_response("items/add.html",kwvars)
		else:
			info = items_info(host=host,name=name,service=service,path=path,shell=shell,process=process,port=port,status=status,group=group,notes=notes)
			try:
				info.save()
				save_log(request.user,"添加应用信息：" + info.name ,"添加成功")		
				return HttpResponseRedirect('/items/info/')
			except Exception,e:
				kwvars = {
					'user':request.user,
					'log':'应用信息添加失败',
				}
				save_log(request.user,"添加应用信息：" + info.name ,"添加失败")
				return render_to_response("items/add.html",kwvars)

@login_required()	
def items_monitor(request):
	kwvars = {
		'user':request.user,
	}
	return render_to_response("items/items_monitor.html",kwvars)

@login_required() 
def items_logs(request):
	kwvars = {
		'user':request.user,
	}
	return render_to_response("items/items_logs.html",kwvars)
