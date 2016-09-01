#coding:utf8
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
import os,sys,json
import paramiko

from cmdb.models import *
from system.views import save_log

reload(sys)
sys.setdefaultencoding('utf8')

#setting upload dir
upload_dir = os.path.join(sys.path[0],"upload")

@login_required()
def files_info(request):
	file_list = os.listdir(upload_dir)
	kwvars = {
		'user':request.user,
		'file_list':file_list,
	}
	return render_to_response('files/info.html',kwvars)

@login_required
def files_del(request):
	del_list = request.POST.getlist('del')
	if del_list is not None:
		for name in del_list:
			del_file = os.path.join(upload_dir, name)	
			if os.path.isfile(del_file):
				try:
					os.remove(del_file)
					save_log(request.user,"删除文件：" + name,"删除成功")
					return HttpResponseRedirect('/files/info/')
				except Exception,e:
					save_log(request.user,"删除文件：" + name,e) 
					return HttpResponseRedirect('/system/logs/')
			elif os.path.isdir(del_file):
				try:
					#os.removedirs(del_file)
					import shutil
					shutil.rmtree(del_file)
					save_log(request.user,"删除目录：" + name,"删除成功")
					return HttpResponseRedirect('/files/info/')
				except Exception,e:
					save_log(request.user,"删除目录：" + name,e)
					return HttpResponseRedirect('/system/logs/')
			else:
				return HttpResponseRedirect('/files/info/')
	else:
		return HttpResponseRedirect('/files/info/')

@login_required()
def files_upload(request):
	from django import forms 
	class UploadFileForm(forms.Form): 
		title = forms.CharField(max_length=1000000) 
		file = forms.FileField() 
	if request.method == "GET": 
		data='get'
	if request.method == "POST":
		if (request.FILES['t_file']) is not None:
			try:
				f = save_upload_file(request.FILES['t_file']) 
				save_log(request.user,'上传文件:' + f.name,'上传成功')
				return HttpResponseRedirect('/files/info')
			except Exception,e:
				save_log(request.user,'上传文件',e)
	return HttpResponseRedirect('/files/info')

@login_required()	
def files_rsync(request):
	host = request.POST.getlist('ip')
	files = request.POST.getlist('file')
	path = request.POST.get('dir')	
	
	file_list = os.listdir(upload_dir)
	host_list = host_info.objects.all()

	if host is not None and files is not None and path is not None:
		action = []
		for ip in host:
			for file_name in files:
				try:
					action.extend(["File:",files])
					action.extend(["Host:",ip])
					action.extend(["Path:",path])
					files_transfe(ip,file_name,path)
				except Exception,e:
					save_log(request.user,'文件传输:' + ip + files,e)
		kwvars = {
			'user':request.user,
			'file_list':file_list,
			'host_list':host_list,
			'logs':action,	
		}
		return render_to_response('files/rsync.html',kwvars)
	else:
		kwvars = {
			'user':request.user,
			'file_list':file_list,
			'host_list':host_list,
			'logs':"请选择详细信息:文件名,主机,存放目录",
		}
		return render_to_response('files/rsync.html',kwvars)


def save_upload_file(f):
	#path = upload_dir
	#f_path = path + f.name
	f_path = os.path.join(upload_dir, f.name)
	with open(f_path, 'wb+') as info: 
		#print f.name 
		for chunk in f.chunks(): 
			info.write(chunk) 
	return f 

def files_transfe(host,file_name,remote_dir):
	server = ssh_info.objects.get(ip=host)
	try:
		t=paramiko.Transport((server.ip,int(server.port)))
		t.connect(username=server.username,password=server.password)
		sftp=paramiko.SFTPClient.from_transport(t)
		
		local_file = os.path.join(upload_dir, file_name)	
		remote_file = os.path.join(remote_dir,file_name)
		try:
			sftp.put(local_file,remote_file)
			save_log(server.username,"传输文件:" + local_file + "  |  Host:" + server.ip , "ok")
		except Exception,e:
			save_log(server.username,"传输文件:" + local_file + "  |  Host:" + server.ip , e)
	except Exception,e:
		save_log(server.username,"传输文件:" + local_file + "  |  Host:" + server.ip ,e)

