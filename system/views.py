# Create your views here. 
#coding:utf8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from system.models import *
from cmdb.models import *

import paramiko
import sys

reload(sys)
sys.setdefaultencoding('utf8')

@login_required()
def system_base(request):
	kwvars = {
		'user':request.user,
	}
	return render_to_response("system/base.html",kwvars)


@login_required()
def system_soft(request):
	kwvars = {
		'user':request.user,
	}
	return render_to_response("system/soft.html",kwvars)

@login_required()
def system_reboot(request):
	kwvars = {
		'user':request.user,
	}
	return render_to_response("system/reboot.html",kwvars)

@login_required()
def system_check(request):
	kwvars = {
		'user':request.user,
	}
	return render_to_response("system/check.html",kwvars)

@login_required()
def system_monitor(request):
	kwvars = {
		'user':request.user,
	}
	return render_to_response("system/monitor.html",kwvars)

@login_required()
def system_logs(request):
	log_list = sys_logs.objects.order_by("-id")
	kwvars = {
		'user':request.user,
		'log_list':log_list,
	}
	return render_to_response("system/logs.html",kwvars)


@login_required()
def system_shell(request):
	host = request.POST.getlist('ip')
	cmd = request.POST.get('command')
	ssh_list = ssh_info.objects.all()
	if host is not None and cmd is not None:
		result = []
		for i in host:
			result.extend(["主机IP:",i])
			result.extend(["执行命令:",cmd])
			result.append("执行结果:")
			try:
				result.extend(remote_shell(request.user,i,cmd))
				#save_log(request.user,'主机：' + i + '|' + '执行命令：' + cmd ,"执行成功")
			except Exception,e:
				save_log(request.user,'主机：' + i + '|' + '执行命令：' + cmd ,e)	
		kwvars = {
			'user':request.user,
			'ssh_list':ssh_list,
			'result':result,
			'host':host
		}
		return render_to_response('remote_shell.html',kwvars)
	else:
		kwvars = {
			'user':request.user,
			'ssh_list':ssh_list,
			'log':"请选择主机并输入要执行的命令！！！",
		}
		return render_to_response('remote_shell.html',kwvars)

@login_required()
def system_mail(request):
	mail_conf = mail_info.objects.all()

	save = request.GET.get('save')
	edit = request.GET.get('edit')
	remove = request.GET.get('remove')
	send = request.GET.get('send')

	mail_host = request.POST.get('mail_host')
	mail_port = request.POST.get('mail_port')
	mail_user = request.POST.get('mail_user')
	mail_pass = request.POST.get('mail_pass')
	mail_postfix = request.POST.get('mail_postfix')
	to_list = request.POST.get('to_list')
	if save:
		sql = mail_info(id=save,mail_host=mail_host,mail_port=mail_port,mail_user=mail_user,mail_pass=mail_pass,mail_postfix=mail_postfix,to_list=to_list)
		try:
			sql.save()
			save_log(request.user,"Mail config","ok")
			return HttpResponseRedirect('/system/mail/')
		except Exception,e:
			save_log(request.user,"Mail config",e)
			
	elif edit:
		mail_conf = mail_info.objects.get(id=edit)
		kwvars = {
			'user':request.user,
			'mail_info':mail_conf,
		}
		return render_to_response('system/mail_edit.html',kwvars)
	elif remove:
		del_sql = mail_info.objects.filter(id=remove)
		del_sql.delete()
		save_log(request.user,"remove mail conf","ok")
		return HttpResponseRedirect('/system/mail/')
	elif send:
		res = send_mail("测试","此邮件为测试发送~~")
		kwvars = {
			'user':request.user,
			'mail_info':mail_conf,
			#'res':res,
		}
		return render_to_response('system/system_mail.html',kwvars)	
	elif not mail_conf:
		kwvars = {
			'user':request.user,
		}
		return render_to_response('system/mail_conf.html',kwvars)
	else:
		kwvars = {
			'user':request.user,
			'mail_info':mail_conf,
		}
		return render_to_response('system/system_mail.html',kwvars)

def save_log(username,action,result):
	log_sql = sys_logs(username=username,action=action,result=result)
	try:
		log_sql.save()
	except Exception,e:
		return e

def send_mail(subject,context):
	import smtplib
	import os,sys
	from email.mime.text import MIMEText
	from email.header import Header
	mail_conf = mail_info.objects.get(id=1)

	msg = MIMEText(context,'plain','utf-8')
	msg['From'] = Header("Auto OPS")
	msg['To'] = ";".join((mail_conf.to_list).split(";"))
	msg['Subject'] = Header(subject, 'utf-8')
	
	send_smtp = smtplib.SMTP()
	send_smtp.connect(mail_conf.mail_host, int(mail_conf.mail_port))
	send_smtp.login(mail_conf.mail_user, mail_conf.mail_pass)
	try:
		for list in (mail_conf.to_list).split(";"):
			send_smtp.sendmail(mail_conf.mail_user, list, msg.as_string())
		send_smtp.close()
		return True
	except Exception, e:
		print str(e)
		return False

def check_port(host,port):
	import os,socket
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		s.connect((host,int(port)))
		s.shutdown(2)
		return True
	except:
		return False

def remote_shell(user,host,cmd):
	server = ssh_info.objects.get(ip=host) 
	s=paramiko.SSHClient()
	s.load_system_host_keys()
	s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		s.connect(hostname=server.ip,port=int(server.port),username=server.username,password=server.password)
		stdin,stdout,stderr=s.exec_command(cmd)
		save_log(user,'主机：' + host + '  |  ' + '执行命令：' + cmd ,"执行成功")
		#print stdout.read()
		res = []
		res = stdout.readlines()
		s.close()
		return res
	except Exception,e:
		save_log(user,'主机：' + host + '  |  ' + '执行命令：' + cmd ,e)
		#res = e
		#return res
		return e

