#!/bin/bash
#
backup_dir="/home/backup"
project_dir="/home/project"
project_name="DevOPS"

[[ -d ${backup_dir} ]] && cd ${project_dir} || mkdir -p ${backup_dir}
[[ -d ${project_dir} ]] || exit 0
[[ -f ${backup_dir}/${project_name}_`date +%Y%m%d`.tar.gz ]] || tar -zcvf ${backup_dir}/${project_name}_`date +%Y%m%d`.tar.gz --exclude=upload ${project_name}
