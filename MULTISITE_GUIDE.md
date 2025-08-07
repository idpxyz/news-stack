# Wagtail 多站点操作指南

## 🎯 概述

本指南详细介绍如何在 Wagtail 多站点新闻平台中创建、管理和配置多个站点。

## 🚀 快速创建站点

### 使用管理命令（推荐）

```bash
# 创建新闻站点（带示例内容）
python manage.py create_site news.local "新闻站点" --create-content

# 创建体育站点
python manage.py create_site sports.local "体育站点" --port 9000

# 创建科技站点（设为默认）
python manage.py create_site tech.local "科技站点" --default

# 创建娱乐站点
python manage.py create_site entertainment.local "娱乐站点" --create-content
```

### 命令参数说明

- `hostname`: 站点域名（如 news.local）
- `site_name`: 站点显示名称
- `--port`: 端口号（默认 9000）
- `--default`: 设为默认站点
- `--create-content`: 创建示例内容

## ⚙️ 环境配置

### 1. 配置 hosts 文件

#### Windows

编辑 `C:\Windows\System32\drivers\etc\hosts`

```bash
127.0.0.1 news.local
127.0.0.1 sports.local
127.0.0.1 tech.local
127.0.0.1 entertainment.local
```

#### Linux/Mac

编辑 `/etc/hosts`

```bash
127.0.0.1 news.local
127.0.0.1 sports.local
127.0.0.1 tech.local
127.0.0.1 entertainment.local
```

### 2. 更新 Django 设置

在 `settings.py` 中添加域名：

```python
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "news.local",
    "sports.local",
    "tech.local",
    "entertainment.local"
]
```

## 🌐 访问站点

### 启动开发服务器

```bash
python manage.py runserver 0.0.0.0:9000
```

### 访问不同站点

```
http://news.local:9000/           # 新闻站点
http://sports.local:9000/         # 体育站点
http://tech.local:9000/           # 科技站点
http://entertainment.local:9000/  # 娱乐站点

# 管理后台（所有站点共享）
http://localhost:9000/admin/
```

## 📝 站点内容管理

### 查看现有站点

```python
# Django shell
python manage.py shell

>>> from wagtail.models import Site
>>> sites = Site.objects.all()
>>> for site in sites:
...     print(f"{site.hostname}:{site.port} - {site.site_name}")
```

### 为特定站点创建内容

```python
# 获取特定站点
site = Site.objects.get(hostname="news.local")
root_page = site.root_page

# 创建分类页面
from news.models import SectionIndexPage
section = SectionIndexPage(title="新闻分类")
root_page.add_child(instance=section)
section.save_revision().publish()

# 创建文章
from news.models import ArticlePage
from django.utils import timezone

article = ArticlePage(
    title="新闻站点文章",
    date=timezone.now()
)
section.add_child(instance=article)
article.save_revision().publish()
```

## 🎨 站点定制

### 站点特定设置

```python
# 在 core/models.py 中添加
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.admin.panels import FieldPanel

@register_setting
class SiteSpecificSettings(BaseSiteSetting):
    site_logo = models.ImageField(upload_to='site_logos/', blank=True)
    site_description = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    theme_color = models.CharField(max_length=7, default="#007bff")

    panels = [
        FieldPanel('site_logo'),
        FieldPanel('site_description'),
        FieldPanel('contact_email'),
        FieldPanel('theme_color'),
    ]
```

### 站点特定模板

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
  <head>
    <title>
      {% if page.site %}{{ page.site.site_name }} - {% endif %}{{ page.title }}
    </title>
    <style>
      .site-header {
          background-color: {{ settings.core.SiteSpecificSettings.theme_color }};
      }
    </style>
  </head>
  <body>
    <header class="site-header">
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

## 🔧 站点管理命令

### 查看站点信息

```bash
# 查看所有站点
python manage.py shell
>>> from wagtail.models import Site
>>> Site.objects.all().values('hostname', 'port', 'site_name', 'is_default_site')
```

### 删除站点

```python
# 删除特定站点
site = Site.objects.get(hostname="old-site.local")
site.delete()
```

### 修改站点设置

```python
# 修改站点信息
site = Site.objects.get(hostname="news.local")
site.site_name = "新新闻站点"
site.save()
```

## 👥 多站点权限管理

### 权限管理概述

在 Wagtail 多站点系统中，权限管理分为几个层次：

1. **超级用户 (Superuser)**: 拥有所有站点的所有权限
2. **全局权限**: 通过 Django 的 `is_staff` 和全局权限分配
3. **站点特定权限**: 通过 `GroupSitePermission` 为特定站点分配权限
4. **页面级权限**: 通过 `GroupPagePermission` 为特定页面分配权限

### 权限管理命令

#### 设置默认权限结构

```bash
# 为所有站点创建权限组
python manage.py setup_site_permissions
```

#### 查看站点和用户权限

```bash
# 查看所有可用站点
python manage.py setup_site_permissions --list-sites

# 查看所有用户及其权限
python manage.py setup_site_permissions --list-users
```

#### 为特定用户分配站点权限

```bash
# 为用户分配站点管理员权限
python manage.py setup_site_permissions --site news.local --user newsadmin --role admin

# 为用户分配站点编辑权限
python manage.py setup_site_permissions --site sports.local --user sporteditor --role editor

# 为用户分配站点发布权限
python manage.py setup_site_permissions --site tech.local --user techpublisher --role publisher
```

### 角色权限说明

#### 管理员 (admin)

- 添加、编辑、删除页面
- 发布页面
- 管理站点设置
- 管理集合

#### 编辑者 (editor)

- 添加、编辑页面
- 发布页面

#### 发布者 (publisher)

- 编辑页面
- 发布页面

#### 审核者 (moderator)

- 编辑页面
- 发布页面

### 权限管理示例

#### 创建站点专用管理员

```bash
# 1. 创建用户
python manage.py createsuperuser --username newsadmin --email news@example.com

# 2. 分配站点权限
python manage.py setup_site_permissions --site news.local --user newsadmin --role admin

# 3. 验证权限
python manage.py setup_site_permissions --list-users
```

#### 创建多个站点的编辑者

```bash
# 创建用户
python manage.py createsuperuser --username multieditor --email editor@example.com

# 分配多个站点权限
python manage.py setup_site_permissions --site news.local --user multieditor --role editor
python manage.py setup_site_permissions --site sports.local --user multieditor --role editor
```

### 权限验证

#### 在 Django Shell 中验证权限

```python
# 进入 Django shell
python manage.py shell

# 导入必要模块
from django.contrib.auth import get_user_model
from wagtail.models import Site, GroupSitePermission
from wagtail.permission_policies.pages import page_permission_policy

User = get_user_model()

# 获取用户和站点
user = User.objects.get(username='newsadmin')
site = Site.objects.get(hostname='news.local')

# 检查用户是否有站点权限
site_permissions = GroupSitePermission.objects.filter(
    group__user=user,
    site=site
)
print(f"User {user.username} has {site_permissions.count()} permissions for {site.hostname}")

# 检查页面权限
has_add_permission = page_permission_policy.user_has_permission(user, 'add')
print(f"User can add pages: {has_add_permission}")
```

#### 在管理后台验证权限

1. 使用分配了权限的用户登录管理后台
2. 检查是否只能看到和编辑指定站点的内容
3. 验证权限限制是否生效

### 高级权限配置

#### 自定义权限组

```python
# 在 Django shell 中创建自定义权限
from django.contrib.auth.models import Group, Permission
from wagtail.models import Site, GroupSitePermission

# 创建自定义组
custom_group = Group.objects.create(name="新闻站点_高级编辑")

# 获取特定权限
add_page_perm = Permission.objects.get(
    codename='add_page',
    content_type__app_label='wagtailcore'
)

# 为特定站点分配权限
site = Site.objects.get(hostname='news.local')
GroupSitePermission.objects.create(
    group=custom_group,
    site=site,
    permission=add_page_perm
)
```

#### 页面级权限

```python
# 为特定页面分配权限
from wagtail.models import GroupPagePermission, Page

# 获取页面和组
page = Page.objects.get(slug='news-article')
group = Group.objects.get(name='新闻站点_编辑者')

# 分配页面权限
GroupPagePermission.objects.create(
    group=group,
    page=page,
    permission_type='edit'  # 'add', 'edit', 'publish', 'bulk_delete', 'lock', 'unlock'
)
```

### 权限最佳实践

1. **最小权限原则**: 只分配用户工作所需的最小权限
2. **角色分离**: 为不同角色创建不同的权限组
3. **定期审查**: 定期检查和更新用户权限
4. **权限文档**: 记录每个角色的权限范围
5. **测试权限**: 在分配权限后测试是否按预期工作

### 常见权限问题

#### 用户无法访问管理后台

```bash
# 检查用户是否为staff
python manage.py shell
>>> user = User.objects.get(username='username')
>>> user.is_staff = True
>>> user.save()
```

#### 用户无法编辑特定站点内容

```bash
# 检查站点权限
python manage.py setup_site_permissions --list-users

# 重新分配权限
python manage.py setup_site_permissions --site site.local --user username --role editor
```

#### 权限不生效

```python
# 清除权限缓存
from django.core.cache import cache
cache.clear()

# 重新登录用户
# 在管理后台重新登录
```

## 🚀 生产环境部署

### Nginx 配置

```nginx
# /etc/nginx/sites-available/news.local
server {
    listen 80;
    server_name news.local;

    location /static/ {
        alias /path/to/your/staticfiles/;
    }

    location /media/ {
        alias /path/to/your/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# 启用站点
sudo ln -s /etc/nginx/sites-available/news.local /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Docker 配置

```yaml
# docker-compose.yml
version: "3.8"

services:
  web:
    build: .
    ports:
      - "9000:9000"
    environment:
      - ALLOWED_HOSTS=news.local,sports.local,tech.local,entertainment.local
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

## 📊 站点监控

### 站点访问统计

```python
# 创建站点访问统计模型
from django.db import models
from wagtail.models import Site

class SiteVisit(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    visited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-visited_at']
```

### 站点性能监控

```python
# 在中间件中添加站点性能监控
import time
from django.utils.deprecation import MiddlewareMixin

class SitePerformanceMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            site = getattr(request, 'site', None)
            if site:
                print(f"Site: {site.hostname}, Response time: {duration:.3f}s")
        return response
```

## ❓ 常见问题

### 1. 站点无法访问

```bash
# 检查hosts文件配置
cat /etc/hosts | grep news.local

# 检查Django设置
python manage.py shell
>>> from django.conf import settings
>>> print(settings.ALLOWED_HOSTS)
```

### 2. 站点内容不显示

```python
# 检查站点根页面
site = Site.objects.get(hostname="news.local")
print(f"Root page: {site.root_page.title}")
print(f"Root page live: {site.root_page.live}")
```

### 3. 管理后台无法访问

```bash
# 确保使用localhost访问管理后台
http://localhost:9000/admin/
```

## 🎯 最佳实践

1. **域名规划**: 使用有意义的域名，如 news.local, sports.local
2. **内容分离**: 为不同站点创建独立的内容结构
3. **设置管理**: 使用站点特定设置管理每个站点的配置
4. **性能优化**: 为每个站点配置独立的缓存策略
5. **监控告警**: 设置站点可用性监控和性能告警

---

**注意**: 本指南适用于开发环境，生产环境请根据实际情况调整配置。
