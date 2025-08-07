# Wagtail 多站点新闻平台开发指导

## 📋 目录

1. [项目概述](#项目概述)
2. [环境要求](#环境要求)
3. [快速开始](#快速开始)
4. [开发环境配置](#开发环境配置)
5. [项目结构详解](#项目结构详解)
6. [开发工作流程](#开发工作流程)
7. [测试指南](#测试指南)
8. [部署指南](#部署指南)
9. [常见问题](#常见问题)
10. [最佳实践](#最佳实践)

## 🎯 项目概述

这是一个基于 Wagtail CMS 的多站点新闻平台，支持多频道、文章管理、首页模块编排、审核工作流等功能。

### 核心特性

- **多站点支持**：可管理多个独立的新闻站点
- **25 个中文频道**：参考今日头条的频道分类
- **模块化首页**：灵活的首页内容编排
- **API 优先设计**：支持前后端分离
- **现代化技术栈**：Wagtail + Django + Next.js

### 频道分类

- **新闻类**：推荐、热点、国际、社会、军事
- **科技类**：科技、数码、科学
- **财经类**：财经、汽车、房产
- **生活类**：健康、教育、时尚、美食、旅游
- **娱乐类**：娱乐、游戏、体育
- **专业类**：母婴、宠物、历史、文化、环保、公益

## 💻 环境要求

### 必需软件

- **Python 3.8+** (推荐 3.12)
- **Node.js 16+** (用于 Next.js 前端)
- **Git**
- **数据库**：SQLite (开发) / PostgreSQL (生产)

### 可选软件

- **Redis** (缓存和会话)
- **OpenSearch** (全文搜索)
- **Docker** (容器化部署)

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd news-stack
```

### 2. 设置虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
.\venv\Scripts\Activate.ps1

# 激活虚拟环境 (Linux/Mac)
source venv/bin/activate
```

### 3. 安装依赖

```bash
# 升级pip
python -m pip install --upgrade pip

# 安装Python依赖
pip install -r requirements.txt
```

### 4. 环境配置

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑环境变量
# 根据需要修改 .env 文件
```

### 5. 数据库初始化

```bash
# 创建数据库迁移
python manage.py makemigrations

# 应用迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

### 6. 生成演示数据

```bash
# 初始化站点
python manage.py bootstrap_sites

# 生成演示数据
python manage.py seed_demo

# 设置工作流
python manage.py setup_workflow
```

### 7. 启动开发服务器

```bash
# 启动Django服务器
python manage.py runserver 0.0.0.0:9000

# 访问地址
# 前台: http://localhost:9000/
# 管理后台: http://localhost:9000/admin/
```

## ⚙️ 开发环境配置

### 环境变量配置 (.env)

```bash
# Django设置
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=1

# 数据库配置
DATABASE_URL=postgresql://user:pass@localhost/dbname

# Redis缓存
REDIS_URL=redis://localhost:6379/0

# OpenSearch搜索
OS_ENABLED=1
OS_URL=http://localhost:9200
OS_INDEX=news_articles

# 邮件设置
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### IDE 配置推荐

#### VS Code 配置

```json
{
  "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "python.testing.pytestEnabled": true
}
```

#### PyCharm 配置

1. 设置项目解释器为虚拟环境
2. 配置 Django 支持
3. 设置代码风格为 PEP 8

## 📁 项目结构详解

```
news-stack/
├── 📁 venv/                    # Python虚拟环境
├── 📁 news_platform/           # Django主项目配置
│   ├── 📄 settings.py          # 项目设置
│   ├── 📄 urls.py              # URL路由
│   ├── 📄 wsgi.py              # WSGI配置
│   └── 📄 asgi.py              # ASGI配置
├── 📁 news/                    # 新闻应用模块
│   ├── 📄 models.py            # 数据模型
│   ├── 📄 apps.py              # 应用配置
│   └── 📁 management/          # 管理命令
├── 📁 core/                    # 核心功能模块
│   ├── 📄 models.py            # 首页和设置模型
│   ├── 📄 wagtail_hooks.py     # Wagtail钩子
│   └── 📁 management/          # 管理命令
├── 📁 authapp/                 # 认证应用
│   ├── 📄 views.py             # 认证视图
│   └── 📄 urls.py              # 认证URL
├── 📁 portal/                  # API接口模块
│   └── 📄 views.py             # API视图
├── 📁 portal_next/             # Next.js前端
│   ├── 📄 package.json         # Node.js依赖
│   ├── 📄 next.config.js       # Next.js配置
│   └── 📁 pages/               # 页面组件
├── 📁 static/                  # 静态文件
│   ├── 📄 site.css             # 全局样式
│   └── 📄 react-island.js      # React组件
├── 📁 templates/               # Django模板
│   ├── 📄 base.html            # 基础模板
│   ├── 📁 core/                # 核心模板
│   ├── 📁 news/                # 新闻模板
│   └── 📁 fragments/           # 模板片段
├── 📄 manage.py                # Django管理脚本
├── 📄 requirements.txt         # Python依赖
├── 📄 .env                     # 环境变量
└── 📄 README.md                # 项目说明
```

### 核心模块说明

#### news_platform/ - Django 主项目

- **settings.py**: 项目核心配置，包含数据库、缓存、中间件等设置
- **urls.py**: 定义项目的 URL 路由规则
- **wsgi.py/asgi.py**: Web 服务器网关接口

#### news/ - 新闻内容管理

- **Channel**: 新闻频道（科技、体育、娱乐等）
- **ArticlePage**: 文章页面模型
- **SectionIndexPage**: 分类索引页面
- **ChannelsIndexPage**: 频道列表页面

#### core/ - 核心功能和首页

- **HomePage**: 首页模型，支持模块化内容编排
- **HomeToggles**: 首页设置（全局配置）
- **ChannelModuleBlock**: 频道内容模块
- **FeaturedItem**: 首页精选文章

#### authapp/ - 用户认证和权限

- 用户登录/注册
- 权限管理
- OIDC 集成（Logto）
- JWT 令牌处理

#### portal/ - API 接口

- RESTful API 接口
- 文章数据 API
- 频道数据 API
- 前端数据接口

#### portal_next/ - Next.js 现代化前端

- SSR/ISR 渲染
- 现代化 UI 组件
- 响应式设计
- 性能优化

## 🔄 开发工作流程

### 1. 多站点管理

#### 多站点架构说明

本项目支持多站点架构，每个站点可以：

- 拥有独立的首页和内容
- 使用不同的域名或子域名
- 共享相同的频道和文章系统
- 独立的内容管理权限

#### 创建新站点

##### 方法一：使用管理命令

```bash
# 创建示例站点
python manage.py bootstrap_sites

# 查看现有站点
python manage.py shell
>>> from wagtail.models import Site
>>> Site.objects.all()
```

##### 方法二：通过 Django Shell 创建

```python
# 进入Django shell
python manage.py shell

# 导入必要模块
from wagtail.models import Page, Site
from core.models import HomePage

# 创建新站点
def create_site(hostname, site_name, port=9000, is_default=False):
    root = Page.get_first_root_node()

    # 检查站点是否已存在
    if Site.objects.filter(hostname=hostname, port=port).exists():
        print(f"Site already exists: {hostname}:{port}")
        return

    # 创建首页
    home = HomePage(title=site_name)
    root.add_child(instance=home)
    home.save_revision().publish()

    # 创建站点
    Site.objects.create(
        hostname=hostname,
        port=port,
        site_name=site_name,
        root_page=home,
        is_default_site=is_default
    )
    print(f"Created site: {hostname}:{port}")

# 创建新站点示例
create_site("news.local", "新闻站点", port=9000)
create_site("sports.local", "体育站点", port=9000)
create_site("tech.local", "科技站点", port=9000)
```

##### 方法三：通过管理后台

1. 访问 `http://localhost:9000/admin/`
2. 进入 "Sites" 管理页面
3. 点击 "Add site"
4. 填写站点信息：
   - **Hostname**: 站点域名（如 news.local）
   - **Port**: 端口号（默认 9000）
   - **Site name**: 站点显示名称
   - **Root page**: 选择根页面
   - **Is default site**: 是否设为默认站点

#### 站点配置示例

##### 开发环境配置

```bash
# 在 .env 文件中添加站点域名
ALLOWED_HOSTS=localhost,127.0.0.1,news.local,sports.local,tech.local

# 或在 settings.py 中配置
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "news.local",
    "sports.local",
    "tech.local"
]
```

##### 本地 hosts 文件配置

```bash
# Windows: C:\Windows\System32\drivers\etc\hosts
# Linux/Mac: /etc/hosts

127.0.0.1 news.local
127.0.0.1 sports.local
127.0.0.1 tech.local
127.0.0.1 media1.local
127.0.0.1 media2.local
```

#### 访问不同站点

```bash
# 启动开发服务器
python manage.py runserver 0.0.0.0:9000

# 访问不同站点
http://news.local:9000/      # 新闻站点
http://sports.local:9000/    # 体育站点
http://tech.local:9000/      # 科技站点
http://media1.local:9000/    # 媒体站点1
http://media2.local:9000/    # 媒体站点2

# 管理后台（所有站点共享）
http://localhost:9000/admin/
```

#### 站点内容管理

##### 为不同站点创建内容

```python
# 在Django shell中为特定站点创建内容
from wagtail.models import Site
from news.models import ArticlePage, SectionIndexPage

# 获取特定站点
site = Site.objects.get(hostname="news.local")
root_page = site.root_page

# 创建分类页面
section = SectionIndexPage(title="新闻分类")
root_page.add_child(instance=section)
section.save_revision().publish()

# 创建文章
article = ArticlePage(
    title="新闻站点文章",
    date=timezone.now()
)
section.add_child(instance=article)
article.save_revision().publish()
```

##### 站点特定设置

```python
# 在 core/models.py 中添加站点特定设置
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

@register_setting
class SiteSpecificSettings(BaseSiteSetting):
    site_logo = models.ImageField(upload_to='site_logos/', blank=True)
    site_description = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)

    panels = [
        FieldPanel('site_logo'),
        FieldPanel('site_description'),
        FieldPanel('contact_email'),
    ]
```

#### 多站点 API 开发

##### 站点感知的 API

```python
# 在 portal/views.py 中创建站点感知的API
from rest_framework.decorators import api_view
from rest_framework.response import Response
from wagtail.models import Site

@api_view(['GET'])
def api_site_home(request):
    # 获取当前请求的站点
    site = request.site

    data = {
        "site_name": site.site_name,
        "hostname": site.hostname,
        "port": site.port,
        "root_page": site.root_page.title,
        "is_default": site.is_default_site
    }

    return Response(data)

@api_view(['GET'])
def api_site_articles(request):
    # 获取当前站点的文章
    site = request.site
    root_page = site.root_page

    articles = ArticlePage.objects.live().descendant_of(root_page)[:10]

    data = {
        "site": site.site_name,
        "articles": [
            {
                "title": article.title,
                "url": article.get_url(),
                "date": article.date
            }
            for article in articles
        ]
    }

    return Response(data)
```

#### 多站点模板开发

##### 站点特定模板

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
  <head>
    <title>
      {% if page.site %}{{ page.site.site_name }} - {% endif %}{{ page.title }}
    </title>
  </head>
  <body>
    <header>
      <h1>{{ request.site.site_name }}</h1>
      <p>当前站点: {{ request.site.hostname }}:{{ request.site.port }}</p>
    </header>

    <main>{% block content %}{% endblock %}</main>

    <footer>
      <p>&copy; {{ request.site.site_name }}</p>
    </footer>
  </body>
</html>
```

##### 站点特定样式

```css
/* static/site-specific.css */
.site-news {
  background-color: #e3f2fd;
}

.site-sports {
  background-color: #f3e5f5;
}

.site-tech {
  background-color: #e8f5e8;
}
```

#### 多站点部署配置

##### Nginx 多站点配置

```nginx
# /etc/nginx/sites-available/news.local
server {
    listen 80;
    server_name news.local;

    location / {
        proxy_pass http://127.0.0.1:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# /etc/nginx/sites-available/sports.local
server {
    listen 80;
    server_name sports.local;

    location / {
        proxy_pass http://127.0.0.1:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

##### Docker 多站点配置

```yaml
# docker-compose.yml
version: "3.8"

services:
  web:
    build: .
    ports:
      - "9000:9000"
    environment:
      - ALLOWED_HOSTS=news.local,sports.local,tech.local
    volumes:
      - ./static:/app/static
      - ./media:/app/media

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web
```

### 2. 功能开发流程

#### 添加新功能模块

```bash
# 创建新的Django应用
python manage.py startapp new_module

# 在settings.py中注册应用
INSTALLED_APPS = [
    ...
    "new_module",
]

# 创建数据模型
# 编辑 new_module/models.py

# 创建迁移
python manage.py makemigrations new_module

# 应用迁移
python manage.py migrate
```

#### 添加新的内容模型

```python
# 在 news/models.py 中添加新模型
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel

class NewContentPage(Page):
    content = models.TextField()

    content_panels = Page.content_panels + [
        FieldPanel("content"),
    ]

    parent_page_types = ["news.SectionIndexPage"]
    subpage_types = []
```

#### 创建 API 接口

```python
# 在 portal/views.py 中添加API视图
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_new_feature(request):
    data = {
        "message": "New feature API",
        "status": "success"
    }
    return Response(data)
```

### 2. 前端开发流程

#### Next.js 开发

```bash
# 进入Next.js目录
cd portal_next

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

#### 添加新页面

```jsx
// portal_next/pages/new-page.js
export default function NewPage() {
  return (
    <div>
      <h1>新页面</h1>
    </div>
  );
}
```

### 3. 数据库操作

#### 创建迁移

```bash
# 为特定应用创建迁移
python manage.py makemigrations news

# 为所有应用创建迁移
python manage.py makemigrations
```

#### 应用迁移

```bash
# 应用所有迁移
python manage.py migrate

# 应用特定应用的迁移
python manage.py migrate news
```

#### 数据操作

```bash
# 进入Django shell
python manage.py shell

# 示例：创建频道
from news.models import Channel
Channel.objects.create(name="新频道", slug="new-channel")
```

### 4. 内容管理

#### 管理后台操作

1. 访问 `http://localhost:9000/admin/`
2. 使用超级用户登录
3. 管理页面、文章、频道等

#### 批量操作

```bash
# 重新生成演示数据
python manage.py seed_demo

# 重建搜索索引
python manage.py reindex_opensearch
```

## 🧪 测试指南

### 1. 单元测试

#### 运行测试

```bash
# 运行所有测试
python manage.py test

# 运行特定应用的测试
python manage.py test news

# 运行特定测试文件
python manage.py test news.tests.test_models

# 运行特定测试方法
python manage.py test news.tests.test_models.ChannelModelTest.test_channel_creation
```

#### 编写测试

```python
# news/tests.py
from django.test import TestCase
from news.models import Channel

class ChannelModelTest(TestCase):
    def test_channel_creation(self):
        channel = Channel.objects.create(
            name="测试频道",
            slug="test-channel"
        )
        self.assertEqual(channel.name, "测试频道")
        self.assertTrue(channel.is_active)
```

### 2. 集成测试

#### API 测试

```python
from rest_framework.test import APITestCase
from django.urls import reverse

class APITest(APITestCase):
    def test_api_home(self):
        url = reverse('api-home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
```

### 3. 前端测试

#### Next.js 测试

```bash
# 运行前端测试
cd portal_next
npm test

# 运行测试覆盖率
npm run test:coverage
```

### 4. 性能测试

#### 使用 Django Debug Toolbar

```bash
# 安装调试工具
pip install django-debug-toolbar

# 在settings.py中添加
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
```

## 🚀 部署指南

### 1. 生产环境配置

#### 环境变量

```bash
# 生产环境设置
DJANGO_DEBUG=0
DJANGO_SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@host:port/dbname
REDIS_URL=redis://host:port/0
```

#### 静态文件收集

```bash
# 收集静态文件
python manage.py collectstatic

# 配置静态文件服务
# 使用Nginx或CDN
```

### 2. 数据库配置

#### PostgreSQL 设置

```bash
# 安装PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# 创建数据库
sudo -u postgres createdb news_platform

# 创建用户
sudo -u postgres createuser news_user

# 设置密码
sudo -u postgres psql
ALTER USER news_user PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE news_platform TO news_user;
```

### 3. 服务器配置

#### Nginx 配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /path/to/your/staticfiles/;
    }

    location /media/ {
        alias /path/to/your/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Gunicorn 配置

```bash
# 安装Gunicorn
pip install gunicorn

# 启动命令
gunicorn news_platform.wsgi:application --bind 127.0.0.1:8000 --workers 4
```

### 4. Docker 部署

#### Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "news_platform.wsgi:application", "--bind", "0.0.0.0:8000"]
```

#### docker-compose.yml

```yaml
version: "3.8"

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/news_platform
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=news_platform
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass

  redis:
    image: redis:7-alpine
```

## ❓ 常见问题

### 1. 数据库问题

#### 迁移错误

```bash
# 重置迁移
python manage.py migrate --fake-initial

# 删除迁移文件重新创建
rm news/migrations/0001_initial.py
python manage.py makemigrations news
```

#### 数据库连接问题

```bash
# 检查数据库连接
python manage.py dbshell

# 重置数据库
python manage.py flush
```

### 2. 静态文件问题

#### 静态文件不加载

```bash
# 重新收集静态文件
python manage.py collectstatic --clear

# 检查STATIC_URL设置
# 确保STATICFILES_DIRS配置正确
```

### 3. 权限问题

#### 文件权限

```bash
# 设置正确的文件权限
chmod -R 755 /path/to/project
chmod -R 777 /path/to/media
```

### 4. 端口占用

#### 端口被占用

```bash
# 查看端口占用
netstat -ano | findstr :9000

# 杀死进程
taskkill /PID <process_id> /F
```

### 5. Wagtail 相关问题

#### 工作流错误

```bash
# 如果遇到工作流相关错误，可以简化工作流设置
python manage.py setup_workflow
```

#### 设置命名空间错误

```bash
# 确保在settings.py中包含
INSTALLED_APPS = [
    ...
    "wagtail.contrib.settings",
    ...
]
```

## 🏆 最佳实践

### 1. 代码规范

#### Python 代码规范

- 使用 Black 进行代码格式化
- 遵循 PEP 8 规范
- 使用类型注解
- 编写文档字符串

```bash
# 安装代码格式化工具
pip install black flake8 isort

# 格式化代码
black .
flake8 .
isort .
```

#### 前端代码规范

- 使用 ESLint 和 Prettier
- 遵循 React 最佳实践
- 使用 TypeScript

### 2. 版本控制

#### Git 工作流

```bash
# 创建功能分支
git checkout -b feature/new-feature

# 提交代码
git add .
git commit -m "feat: add new feature"

# 推送分支
git push origin feature/new-feature

# 创建合并请求
```

#### 提交信息规范

- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `style:` 代码格式
- `refactor:` 重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具的变动

### 3. 安全最佳实践

#### 环境变量管理

- 不要将敏感信息提交到版本控制
- 使用环境变量存储配置
- 定期轮换密钥

#### 数据库安全

- 使用强密码
- 限制数据库访问
- 定期备份数据

### 4. 性能优化

#### 数据库优化

- 使用数据库索引
- 优化查询语句
- 使用缓存

#### 前端优化

- 代码分割
- 图片优化
- 使用 CDN

### 5. 监控和日志

#### 日志配置

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 🔧 常用命令速查

### Django 管理命令

```bash
# 开发服务器
python manage.py runserver 0.0.0.0:9000

# 数据库操作
python manage.py makemigrations
python manage.py migrate
python manage.py dbshell

# 用户管理
python manage.py createsuperuser
python manage.py changepassword

# 静态文件
python manage.py collectstatic

# 测试
python manage.py test
python manage.py test --coverage

# Shell
python manage.py shell
```

### 项目特定命令

```bash
# 初始化项目
python manage.py bootstrap_sites
python manage.py seed_demo
python manage.py setup_workflow

# 多站点管理
python manage.py create_site news.local "新闻站点" --create-content
python manage.py create_site sports.local "体育站点" --port 9000
python manage.py create_site tech.local "科技站点" --default

# 多站点权限管理
python manage.py setup_site_permissions
python manage.py setup_site_permissions --list-sites
python manage.py setup_site_permissions --list-users
python manage.py setup_site_permissions --site news.local --user newsadmin --role admin

# 搜索索引
python manage.py reindex_opensearch
```

### 包管理

```bash
# 安装新包
pip install package_name

# 更新requirements.txt
pip freeze > requirements.txt

# 安装所有依赖
pip install -r requirements.txt
```

## 📚 参考资源

### 官方文档

- [Django 文档](https://docs.djangoproject.com/)
- [Wagtail 文档](https://docs.wagtail.org/)
- [Next.js 文档](https://nextjs.org/docs)

### 社区资源

- [Django 社区](https://www.djangoproject.com/community/)
- [Wagtail 社区](https://wagtail.org/community/)

### 工具推荐

- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/)
- [Django Silk](https://github.com/jazzband/django-silk)
- [Django Extensions](https://django-extensions.readthedocs.io/)

## 📞 技术支持

### 项目文档

- [项目结构详解](PROJECT_STRUCTURE.md)
- [包管理指南](PACKAGE_MANAGEMENT.md)
- [虚拟环境设置](VENV_SETUP.md)

### 联系方式

- 项目 Issues: [GitHub Issues](https://github.com/your-repo/issues)
- 技术讨论: [GitHub Discussions](https://github.com/your-repo/discussions)

---

**注意**：本开发指导会随着项目发展持续更新，请定期查看最新版本。

**最后更新**：2025 年 8 月 7 日
**版本**：1.0.0
