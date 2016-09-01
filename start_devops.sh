#!/bin/bash

mysql_port=3306
mysql_pid=`lsof -i:${mysql_port} | awk '{print $2}' | grep -v PID | uniq `
project_dir="/home/project/DevOPS"

cd ${project_dir} || exit 0
python manage.py makemigrations && python manage.py migrate

if [ ! -z ${mysql_pid} ];then
	echo "Start project DevOPS ..."
	python /home/project/DevOPS/manage.py runserver 0.0.0.0:80
else
	echo ""
	/etc/init.d/mysqld start && python /home/project/DevOPS/manage.py runserver 0.0.0.0:80
fi
