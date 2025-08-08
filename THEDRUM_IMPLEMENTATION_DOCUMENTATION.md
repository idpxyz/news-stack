# The Drum 风格网站实现文档

## 项目概述

本文档记录了基于 Wagtail CMS 7.1 的新闻平台项目，实现 The Drum 风格网站的全过程。项目从基础架构搭建到现代化 UI 设计，涵盖了多站点管理、内容管理系统、前端设计等多个方面。

## 技术栈

- **后端框架**: Django 5.0.14
- **CMS 系统**: Wagtail 7.1
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **前端技术**: HTML5, CSS3, JavaScript
- **模板引擎**: Django Templates
- **静态文件**: Django Static Files
- **包管理**: pip + requirements.txt
- **版本控制**: Git

## 项目结构

```
news-stack/
├── news_platform/          # Django 项目配置
│   ├── settings.py         # 项目设置
│   ├── urls.py            # URL 配置
│   └── wsgi.py            # WSGI 配置
├── core/                   # 核心应用
│   ├── models.py          # 首页和站点设置模型
│   ├── templatetags/      # 自定义模板标签
│   └── management/        # 管理命令
├── news/                   # 新闻应用
│   ├── models.py          # 文章、频道、创意作品等模型
│   └── views.py           # 视图函数
├── authapp/                # 用户认证应用
│   ├── models.py          # 用户资料模型
│   └── views.py           # 认证视图
├── community/              # 社区功能应用
│   ├── models.py          # 讨论、评论等模型
│   └── admin.py           # 管理界面
├── portal/                 # 门户应用
│   └── views.py           # API 视图
├── templates/              # 模板文件
│   ├── base.html          # 基础模板
│   └── core/
│       └── home_page.html # 首页模板
├── static/                 # 静态文件
│   └── site.css           # 主样式文件
├── requirements.txt        # 依赖包列表
├── manage.py              # Django 管理脚本
└── README.md              # 项目说明
```

## 核心功能模块

### 1. 多站点管理系统

#### 1.1 站点模型设计

- 基于 Wagtail 的 `Site` 模型
- 支持多域名配置
- 站点级别的权限管理

#### 1.2 站点设置系统

```python
@register_setting
class SiteTheme(BaseSiteSetting):
    """站点UI主题设置"""
    theme = models.CharField(max_length=20, choices=THEME_CHOICES)
    primary_color = models.CharField(max_length=7, default="#007bff")
    logo_url = models.URLField(blank=True)
    favicon_url = models.URLField(blank=True)
    custom_css = models.TextField(blank=True)
```

#### 1.3 管理命令

- `init_site_settings`: 初始化站点设置
- `create_site`: 创建新站点
- `setup_site_permissions`: 设置站点权限

### 2. 内容管理系统

#### 2.1 文章模型

```python
class ArticlePage(Page):
    date = models.DateTimeField(db_index=True)
    hero_image = models.ForeignKey("wagtailimages.Image")
    body = StreamField(ArticleBody(), use_json_field=True)
    channels = ParentalManyToManyField("news.Channel")
    tags = ClusterTaggableManager(through="news.ArticleTag")
    is_featured = models.BooleanField(default=False)
    feature_rank = models.IntegerField(default=0)
```

#### 2.2 创意作品模型

```python
class CreativeWorkPage(Page):
    """创意作品页面 - 类似The Drum的Creative Works"""
    agency = models.CharField(max_length=200, verbose_name="代理公司")
    client = models.CharField(max_length=200, verbose_name="客户")
    campaign_name = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=20, choices=CREATIVE_CATEGORIES)
    awards = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    project_url = models.URLField(blank=True)
```

#### 2.3 行业活动模型

```python
class IndustryEventPage(Page):
    """行业活动页面 - 类似The Drum的Events"""
    event_date = models.DateTimeField(verbose_name="活动日期")
    end_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200, verbose_name="活动地点")
    organizer = models.CharField(max_length=200, verbose_name="主办方")
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    registration_url = models.URLField(blank=True)
    ticket_price = models.CharField(max_length=100, blank=True)
```

#### 2.4 研究报告模型

```python
class ResearchReportPage(Page):
    """研究报告页面 - 类似The Drum的Research"""
    publish_date = models.DateTimeField(db_index=True)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    author = models.CharField(max_length=200, verbose_name="作者/机构")
    download_url = models.URLField(blank=True)
    is_free = models.BooleanField(default=True)
    summary = models.TextField(verbose_name="报告摘要")
    key_findings = models.TextField(blank=True)
    methodology = models.TextField(blank=True)
```

### 3. 前端设计系统

#### 3.1 设计原则

- **现代化**: 采用卡片式设计、阴影效果、圆角元素
- **响应式**: 支持桌面端和移动端适配
- **交互性**: 悬停效果、动画过渡、微交互
- **可访问性**: 良好的颜色对比、语义化标签

#### 3.2 CSS 架构

```css
/* 设计令牌 */
:root {
  --primary-color: #1a1a1a;
  --secondary-color: #f8f9fa;
  --accent-color: #007bff;
  --text-color: #333;
  --light-text: #666;
  --border-color: #e9ecef;
}

/* 布局系统 */
.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 3rem;
}

/* 组件样式 */
.news-item {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}
```

#### 3.3 页面结构

1. **英雄区域**: 渐变背景、大标题、特色文章轮播
2. **主要内容区**: 新闻网格、创意作品展示、活动列表
3. **侧边栏**: 热门话题、最新讨论、研究报告、订阅区域
4. **底部特色**: 精选内容模块展示

### 4. 模板系统

#### 4.1 基础模板

```html
{% load static wagtailcore_tags %}
<!DOCTYPE html>
<html lang="zh">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>{% block title %}{{ page.title }}{% endblock %} - 新闻平台</title>
    <link rel="stylesheet" href="{% static 'site.css' %}" />
  </head>
  <body>
    <header class="site-header">
      <!-- 导航栏 -->
    </header>

    <main>{% block content %}{% endblock %}</main>

    <footer class="site-footer">
      <!-- 页脚 -->
    </footer>
  </body>
</html>
```

#### 4.2 首页模板

- 英雄区域轮播
- 新闻分类标签
- 内容网格布局
- 侧边栏组件
- 响应式设计

### 5. 数据管理

#### 5.1 频道系统

```python
@register_snippet
class Channel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
```

#### 5.2 标签系统

- 基于 `taggit` 的标签管理
- 支持文章、创意作品、活动等多模型标签
- 标签云和标签页面

#### 5.3 数据初始化

- `init_thedrum_data`: 初始化示例数据
- 包含频道、文章、创意作品、活动、研究报告
- 支持多站点数据初始化

## 开发流程

### 1. 环境搭建

```bash
# 创建虚拟环境
python -m venv venv
.\venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

### 2. 站点配置

```bash
# 初始化站点设置
python manage.py init_site_settings

# 初始化示例数据
python manage.py init_thedrum_data

# 收集静态文件
python manage.py collectstatic --noinput
```

### 3. 开发服务器

```bash
# 启动开发服务器
python manage.py runserver 0.0.0.0:9000
```

## 关键技术实现

### 1. 多站点内容管理

- 使用 Wagtail 的 `Site` 模型进行站点隔离
- 通过 `Site.find_for_request()` 获取当前站点
- 站点级别的设置和权限管理

### 2. 动态内容获取

```python
def get_context(self, request):
    site = Site.find_for_request(request) or Site.objects.filter(is_default_site=True).first()
    site_root = site.root_page

    # 获取特色文章
    featured = ArticlePage.objects.live().public().specific().descendant_of(site_root)

    # 获取创意作品
    creative_works = CreativeWorkPage.objects.live().public().specific().descendant_of(site_root)

    # 获取即将举行的活动
    upcoming_events = IndustryEventPage.objects.live().public().specific().descendant_of(site_root)

    return {
        'featured': featured,
        'creative_works': creative_works,
        'upcoming_events': upcoming_events,
    }
```

### 3. 响应式设计

- CSS Grid 和 Flexbox 布局
- 移动端优先的设计理念
- 断点系统：768px, 1024px, 1200px

### 4. 性能优化

- 静态文件压缩和缓存
- 数据库查询优化
- 图片懒加载
- CDN 集成支持

## 部署配置

### 1. 生产环境设置

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# 静态文件配置
STATIC_ROOT = '/path/to/staticfiles/'
MEDIA_ROOT = '/path/to/media/'
```

### 2. 服务器配置

- Nginx 反向代理
- Gunicorn WSGI 服务器
- Redis 缓存
- PostgreSQL 数据库

## 维护和扩展

### 1. 内容管理

- Wagtail 管理界面
- 工作流和审批系统
- 版本控制和回滚
- 媒体文件管理

### 2. 监控和分析

- Google Analytics 集成
- 错误日志监控
- 性能监控
- 用户行为分析

### 3. 扩展功能

- 搜索功能 (Elasticsearch/OpenSearch)
- 评论系统
- 用户订阅
- 社交媒体集成
- API 接口

## 最佳实践

### 1. 代码组织

- 模块化设计
- 清晰的命名规范
- 代码注释和文档
- 版本控制规范

### 2. 安全考虑

- CSRF 保护
- XSS 防护
- SQL 注入防护
- 文件上传安全
- HTTPS 强制

### 3. 性能优化

- 数据库索引优化
- 缓存策略
- 静态资源优化
- CDN 使用

## 常见问题解决

### 1. 静态文件问题

```bash
# 清除并重新收集静态文件
python manage.py collectstatic --noinput --clear
```

### 2. 数据库迁移问题

```bash
# 重置迁移
python manage.py migrate --fake-initial
```

### 3. 模板缓存问题

```bash
# 清除模板缓存
python manage.py clear_cache
```

## 总结

本项目成功实现了基于 Wagtail CMS 的 The Drum 风格新闻平台，具备以下特点：

1. **现代化设计**: 采用卡片式布局、渐变背景、动画效果
2. **多站点支持**: 完整的站点隔离和权限管理
3. **内容丰富**: 支持文章、创意作品、活动、研究报告等多种内容类型
4. **响应式设计**: 完美适配桌面端和移动端
5. **易于维护**: 清晰的代码结构和完善的文档

项目为新闻媒体和内容平台提供了一个完整的解决方案，可以作为同类项目的基础框架进行扩展和定制。

---

**文档版本**: 1.0  
**最后更新**: 2025 年 8 月  
**维护者**: 开发团队
