[![Build Status](https://travis-ci.com/fish0607/DevOPS.svg?branch=master)](https://travis-ci.com/fish0607/DevOPS)

#### 环境需求
- MySQL-5.6.30
- Python-2.7.11
- Django-1.9.6
- pip 8.1.2
- setuptools-21

#### 依赖库安装
```
pip install -r requirements.txt
```

#### 同步数据库
```
python manage.py makemigrations
python manage.py migrate
```

#### 创建超级用户
```
python manage.py createsuperuser
```

