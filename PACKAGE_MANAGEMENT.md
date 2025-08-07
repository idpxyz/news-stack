# Wagtail 项目包管理指南

## 虚拟环境中的包管理

在虚拟环境中安装和管理包非常简单，所有操作都会自动隔离在 `venv/` 目录下。

## 基本安装命令

### 1. 安装单个包

```bash
pip install package_name
```

### 2. 安装指定版本

```bash
pip install package_name==1.2.3
```

### 3. 安装版本范围

```bash
pip install "package_name>=1.0,<2.0"
```

### 4. 从 requirements 文件安装

```bash
pip install -r requirements.txt
```

### 5. 升级包

```bash
pip install --upgrade package_name
```

## 开发依赖管理

### 安装开发依赖

```bash
# 安装测试框架
pip install pytest pytest-django

# 安装代码格式化工具
pip install black flake8

# 安装调试工具
pip install ipython ipdb

# 安装文档生成工具
pip install sphinx
```

### 创建开发依赖文件

```bash
# 创建开发依赖文件
pip freeze > requirements-dev.txt

# 或者只包含开发工具
echo "pytest==7.4.0" > requirements-dev.txt
echo "black==23.0.0" >> requirements-dev.txt
echo "flake8==6.0.0" >> requirements-dev.txt
```

## 包管理最佳实践

### 1. 更新 requirements.txt

每次安装新包后，更新项目依赖文件：

```bash
pip freeze > requirements.txt
```

### 2. 查看包信息

```bash
# 查看已安装的包
pip list

# 查看特定包信息
pip show package_name

# 查看过时的包
pip list --outdated
```

### 3. 卸载包

```bash
pip uninstall package_name
```

### 4. 检查依赖冲突

```bash
pip check
```

## 常见包安装示例

### Django 相关

```bash
# Django REST framework
pip install djangorestframework

# Django CORS headers
pip install django-cors-headers

# Django Debug Toolbar
pip install django-debug-toolbar

# Django Extensions
pip install django-extensions
```

### 数据库相关

```bash
# MySQL支持
pip install mysqlclient

# SQLite支持（通常已内置）
# 无需额外安装

# MongoDB支持
pip install djongo
```

### 缓存和会话

```bash
# Memcached支持
pip install python-memcached

# Redis支持（已安装）
# django-redis
```

### 文件处理

```bash
# Excel文件处理
pip install openpyxl xlrd

# PDF处理
pip install reportlab PyPDF2

# 图片处理（已安装）
# Pillow
```

### API 和网络

```bash
# HTTP客户端
pip install httpx

# GraphQL支持
pip install graphene-django

# WebSocket支持
pip install channels
```

### 安全和认证

```bash
# OAuth支持
pip install requests-oauthlib

# 密码加密
pip install bcrypt

# JWT（已安装）
# PyJWT
```

### 监控和日志

```bash
# 日志格式化
pip install structlog

# 性能监控
pip install django-silk

# 错误追踪
pip install sentry-sdk
```

## 环境变量管理

### 安装环境变量管理工具

```bash
# python-dotenv（已安装）
pip install python-dotenv

# 或者使用django-environ
pip install django-environ
```

## 测试和调试

### 测试框架

```bash
# pytest（已安装）
pip install pytest pytest-django pytest-cov

# 或者使用Django内置测试
# 无需额外安装
```

### 调试工具

```bash
# IPython增强shell
pip install ipython

# 调试器
pip install ipdb

# 性能分析
pip install line-profiler
```

## 代码质量工具

### 代码格式化

```bash
# Black代码格式化
pip install black

# isort导入排序
pip install isort

# autopep8
pip install autopep8
```

### 代码检查

```bash
# Flake8代码检查
pip install flake8

# Pylint
pip install pylint

# MyPy类型检查
pip install mypy
```

## 部署相关

### 生产环境

```bash
# Gunicorn WSGI服务器
pip install gunicorn

# uWSGI
pip install uwsgi

# 静态文件收集
# python manage.py collectstatic（Django内置）
```

### 容器化

```bash
# Docker相关（通常不需要Python包）
# 使用Dockerfile管理
```

## 注意事项

1. **始终在虚拟环境中安装包**
2. **定期更新 requirements.txt**
3. **避免安装不必要的包**
4. **注意包之间的版本兼容性**
5. **在生产环境中使用固定版本号**

## 故障排除

### 包安装失败

```bash
# 升级pip
python -m pip install --upgrade pip

# 清理缓存
pip cache purge

# 使用国内镜像
pip install package_name -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 依赖冲突

```bash
# 检查冲突
pip check

# 查看依赖树
pip install pipdeptree
pipdeptree
```

### 虚拟环境问题

```bash
# 重新创建虚拟环境
deactivate
rmdir /s venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
