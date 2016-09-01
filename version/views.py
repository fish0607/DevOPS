# Create your views here.
#coding:utf8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import sys
import psutil

from version.models import *
from system.views import save_log

reload(sys)
sys.setdefaultencoding('utf8')

@login_required()
def versioning_show(request):
	svn_list = svn_info.objects.all()
	edit = request.GET.get('edit')
	save = request.GET.get('save')
	update = request.GET.get('update')		
	remove = request.GET.get('remove')
	if edit:
		edit_info = svn_info.objects.get(svn_id=edit)
		kwvars = {
			'user':request.user,
			'info':edit_info,
			'id':edit,
		}
		return render_to_response("version/svn_change.html",kwvars)
	elif save:
		save_id = request.GET.get('save')
		info = svn_info.objects.get(svn_id=save_id)
		info.svn_url = request.POST.get('svn_url')
		info.svn_user = request.POST.get('svn_user')
		info.password = request.POST.get('password')
		info.notes =  request.POST.get('notes')
		try:
			info.save()
			save_log(request.user,"修改版本库信息：" + info.svn_url ,"修改成功" )
			return HttpResponseRedirect('/version/info/')
		except Exception,e:
			kwvars = {
				'user':request.user,
				'log':e,
			}
			save_log(request.user,"修改版本库信息：" + info.svn_url,e)
			return render_to_response("version/svn_change.html",kwvars)
	elif update:
		update_info = svn_info.objects.filter(svn_id=update)
		kwvars = {
			'user':request.user,
			'svn_list':svn_list,
		}
		return render_to_response("version/show.html",kwvars)
	elif remove:
		del_info = svn_info.objects.filter(svn_id=remove)
		try:
			del_info.delete()
			save_log(request.user,"删除版本库：" + remove ,"删除成功" )
			kwvars = {
				'user':request.user,
				'svn_list':svn_list,
			}
			return render_to_response("version/show.html",kwvars)
		except Exception,e:
			kwvars = { 
				'user':request.user,
				'svn_list':svn_list,
				'result':e,
			}
			save_log(request.user,"删除版本库：" + remove ,e )
			return render_to_response("version/show.html",kwvars)
	else:
		kwvars = {
			'user':request.user,
			'svn_list':svn_list,
		}
		return render_to_response("version/show.html",kwvars)	

@login_required()
def versioning_add(request):
	svn_url =  request.POST.get('svn_url')
	svn_user = request.POST.get('svn_user')
	password = request.POST.get('password')
	notes =  request.POST.get('notes')
	if svn_url is not None and svn_user is not None and password is not None:
		sql_info = svn_info(svn_url=svn_url,svn_user=svn_user,password=password,notes=notes)
		try:
			sql_info.save()
			save_log(request.user,"添加版本库：" + svn_url , "添加成功")
			return HttpResponseRedirect('/version/info/')
		except Exception,e:
			kwvars = {
				'user':request.user,
				'result':e,
			}
			save_log(request.user,"添加版本库：" + svn_url , e)
			return render_to_response("version/add.html",kwvars)
	else:
		kwvars = {
			'user':request.user,
			'result':"请输入对应信息！！！",
		}
		return render_to_response("version/add.html",kwvars)
