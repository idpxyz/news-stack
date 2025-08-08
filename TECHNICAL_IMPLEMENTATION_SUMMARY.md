# The Drum 风格网站技术实现总结

## 开发历程概述

本项目从基础 Wagtail CMS 搭建到完整的 The Drum 风格网站实现，历时多个开发阶段，涉及多个技术难点的攻克。本文档重点记录了开发过程中的关键技术问题和解决方案。

## 主要技术挑战与解决方案

### 1. Wagtail 7.1 兼容性问题

#### 问题描述

在开发过程中遇到了多个 Wagtail 7.1 版本兼容性问题：

- `ImageChooserPanel` 被弃用
- `wagtail.contrib.modeladmin` 被移除
- 工作流导入路径变更

#### 解决方案

```python
# 1. 替换 ImageChooserPanel
# 旧代码
from wagtail.images.edit_handlers import ImageChooserPanel
ImageChooserPanel('hero_image')

# 新代码
from wagtail.admin.panels import FieldPanel
FieldPanel('hero_image')

# 2. 移除 modeladmin 依赖
# 旧代码
INSTALLED_APPS = [
    "wagtail.contrib.modeladmin",
]

# 新代码 - 使用 Django Admin
from django.contrib import admin
@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    pass

# 3. 修正工作流导入
# 旧代码
from wagtail.workflows.models import GroupApprovalTask, Workflow

# 新代码
from wagtail.models import GroupApprovalTask, Workflow
```

### 2. 多站点内容隔离

#### 问题描述

需要实现多站点之间的内容完全隔离，确保每个站点只能看到和管理自己的内容。

#### 解决方案

```python
def get_context(self, request):
    # 获取当前站点
    site = Site.find_for_request(request) or Site.objects.filter(is_default_site=True).first()
    if not site:
        return {'featured': [], 'modules': []}

    # 获取站点根页面
    site_root = site.root_page

    # 所有查询都基于站点根页面进行过滤
    featured = ArticlePage.objects.live().public().specific().descendant_of(site_root)
    creative_works = CreativeWorkPage.objects.live().public().specific().descendant_of(site_root)

    return {
        'featured': featured,
        'creative_works': creative_works,
    }
```

### 3. 站点设置系统设计

#### 问题描述

需要为每个站点提供独立的配置选项，包括主题、SEO、广告等设置。

#### 解决方案

```python
@register_setting
class SiteTheme(BaseSiteSetting):
    """站点UI主题设置"""
    THEME_CHOICES = [
        ("default", "默认主题"),
        ("dark", "深色主题"),
        ("light", "浅色主题"),
        ("news", "新闻主题"),
        ("tech", "科技主题"),
    ]

    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default="default")
    primary_color = models.CharField(max_length=7, default="#007bff")
    logo_url = models.URLField(blank=True)
    favicon_url = models.URLField(blank=True)
    custom_css = models.TextField(blank=True)

    panels = [
        MultiFieldPanel([
            FieldPanel("theme"),
            FieldPanel("primary_color"),
        ], heading="主题配置"),
        MultiFieldPanel([
            FieldPanel("logo_url"),
            FieldPanel("favicon_url"),
        ], heading="品牌配置"),
        FieldPanel("custom_css"),
    ]
```

### 4. 模板标签系统

#### 问题描述

需要创建自定义模板标签来在模板中获取站点设置。

#### 解决方案

```python
# core/templatetags/site_settings.py
from django import template
from wagtail.models import Site
from core.models import SiteTheme, SEOSettings, AdSettings, SocialSettings

register = template.Library()

@register.simple_tag(takes_context=True)
def get_site_theme(context):
    """获取站点主题设置"""
    request = context.get('request')
    if not request:
        return None

    site = Site.find_for_request(request) or Site.objects.filter(is_default_site=True).first()
    if not site:
        return None

    try:
        return SiteTheme.for_site(site)
    except SiteTheme.DoesNotExist:
        return None

@register.simple_tag(takes_context=True)
def get_theme_css_class(context):
    """获取主题CSS类名"""
    theme = get_site_theme(context)
    if theme and theme.theme != 'default':
        return f'theme-{theme.theme}'
    return ''
```

### 5. CSS 样式系统重构

#### 问题描述

原有的 CSS 样式无法正确应用，页面显示为基本样式而非现代化的 The Drum 风格。

#### 解决方案

```css
/* 1. 强制样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 2. 设计令牌系统 */
:root {
  --primary-color: #1a1a1a;
  --secondary-color: #f8f9fa;
  --accent-color: #007bff;
  --text-color: #333;
  --light-text: #666;
  --border-color: #e9ecef;
}

/* 3. 现代化布局 */
.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 3rem;
}

/* 4. 卡片式设计 */
.news-item {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.news-item:hover {
  transform: translateY(-5px);
}

/* 5. 响应式设计 */
@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}
```

### 6. 数据库迁移问题

#### 问题描述

在添加新模型和字段时遇到迁移冲突和依赖问题。

#### 解决方案

```bash
# 1. 分步骤创建迁移
python manage.py makemigrations core
python manage.py makemigrations news
python manage.py makemigrations authapp
python manage.py makemigrations community

# 2. 应用迁移
python manage.py migrate

# 3. 如果遇到问题，重置迁移
python manage.py migrate --fake-initial
```

### 7. 静态文件管理

#### 问题描述

静态文件无法正确加载，导致样式不生效。

#### 解决方案

```python
# settings.py
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# 收集静态文件
python manage.py collectstatic --noinput --clear
```

## 核心功能实现细节

### 1. 首页内容动态获取

```python
class HomePage(Page):
    def get_context(self, request):
        from news.models import ArticlePage, CreativeWorkPage, IndustryEventPage, ResearchReportPage
        from django.utils import timezone
        from datetime import timedelta

        ctx = super().get_context(request)

        # 获取站点
        site = Site.find_for_request(request) or Site.objects.filter(is_default_site=True).first()
        if not site:
            ctx["featured"] = []
            ctx["modules"] = []
            ctx["creative_works"] = []
            ctx["upcoming_events"] = []
            ctx["latest_reports"] = []
            ctx["latest_discussions"] = []
            return ctx

        site_root = site.root_page
        selected_ids = set()
        settings = HomeToggles.for_site(site)

        # 获取特色文章
        manual = [fi.article.specific for fi in self.featured_items.select_related("article")]
        manual = [a for a in manual if a.is_descendant_of(site_root)]
        selected_ids |= {a.id for a in manual}

        target = max(0, settings.featured_target - len(manual))
        if target:
            qs = ArticlePage.objects.live().public().specific().descendant_of(site_root)
            if settings.only_with_image_default:
                qs = qs.filter(hero_image__isnull=False)
            if settings.hot_time_window_hours > 0:
                qs = qs.filter(date__gte=timezone.now() - timedelta(hours=settings.hot_time_window_hours))
            qs = qs.exclude(id__in=selected_ids).order_by("-is_featured", "-feature_rank", "-date")[:target]
            backfill = list(qs)
            manual.extend(backfill)
            selected_ids |= {a.id for a in backfill}

        ctx["featured"] = manual

        # 获取创意作品
        creative_works = CreativeWorkPage.objects.live().public().specific().descendant_of(site_root).order_by("-date")[:6]
        ctx["creative_works"] = creative_works

        # 获取即将举行的活动
        upcoming_events = IndustryEventPage.objects.live().public().specific().descendant_of(site_root).filter(
            event_date__gte=timezone.now()
        ).order_by("event_date")[:5]
        ctx["upcoming_events"] = upcoming_events

        # 获取最新研究报告
        latest_reports = ResearchReportPage.objects.live().public().specific().descendant_of(site_root).order_by("-publish_date")[:5]
        ctx["latest_reports"] = latest_reports

        return ctx
```

### 2. 模板系统设计

```html
<!-- templates/core/home_page.html -->
{% extends "base.html" %} {% load static wagtailcore_tags wagtailimages_tags %}
{% block content %}
<!-- 英雄区域 -->
<section class="hero-section">
  <div class="hero-slider">
    {% for article in featured %}
    <div class="hero-slide">
      {% if article.hero_image %}
      <div class="hero-image">{% image article.hero_image fill-1200x600 %}</div>
      {% endif %}
      <div class="hero-content">
        <div class="hero-meta">
          <span class="category"
            >{{ article.channels.first.name|default:"新闻" }}</span
          >
          <span class="date">{{ article.date|date:"M d, Y" }}</span>
        </div>
        <h1 class="hero-title">{{ article.title }}</h1>
        <p class="hero-excerpt">{{ article.specific.body|truncatewords:20 }}</p>
        <a href="{{ article.url }}" class="hero-link">阅读更多</a>
      </div>
    </div>
    {% endfor %}
  </div>
</section>

<!-- 主要内容区域 -->
<div class="main-content">
  <div class="container">
    <div class="content-grid">
      <!-- 左侧内容 -->
      <div class="content-main">
        <!-- 新闻分类标签 -->
        <div class="news-tabs">
          <button class="tab-btn active" data-category="all">全部</button>
          <button class="tab-btn" data-category="brand">品牌</button>
          <button class="tab-btn" data-category="agency">代理</button>
          <button class="tab-btn" data-category="creative">创意</button>
          <button class="tab-btn" data-category="digital">数字</button>
          <button class="tab-btn" data-category="media">媒体</button>
        </div>

        <!-- 最新新闻 -->
        <section class="news-section">
          <h2 class="section-title">最新新闻</h2>
          <div class="news-grid">
            {% for article in modules.0.items %}
            <article class="news-item">
              {% if article.hero_image %}
              <div class="news-image">
                {% image article.hero_image fill-400x250 %}
              </div>
              {% endif %}
              <div class="news-content">
                <div class="news-meta">
                  <span class="category"
                    >{{ article.channels.first.name|default:"新闻" }}</span
                  >
                  <span class="date">{{ article.date|date:"M d" }}</span>
                </div>
                <h3 class="news-title">
                  <a href="{{ article.url }}">{{ article.title }}</a>
                </h3>
                <p class="news-excerpt">
                  {{ article.specific.body|truncatewords:15 }}
                </p>
              </div>
            </article>
            {% endfor %}
          </div>
        </section>

        <!-- 创意作品展示 -->
        <section class="creative-works">
          <h2 class="section-title">创意作品</h2>
          <div class="works-grid">
            {% for work in creative_works %}
            <div class="work-item">
              {% if work.hero_image %}
              <div class="work-image">
                {% image work.hero_image fill-300x200 %}
              </div>
              {% endif %}
              <div class="work-info">
                <h3 class="work-title">
                  <a href="{{ work.url }}">{{ work.title }}</a>
                </h3>
                <p class="work-agency">{{ work.agency }}</p>
                <p class="work-client">{{ work.client }}</p>
              </div>
            </div>
            {% endfor %}
          </div>
        </section>

        <!-- 行业活动 -->
        <section class="events-section">
          <h2 class="section-title">即将举行的活动</h2>
          <div class="events-list">
            {% for event in upcoming_events %}
            <div class="event-item">
              <div class="event-date">
                <span class="day">{{ event.event_date|date:"d" }}</span>
                <span class="month">{{ event.event_date|date:"M" }}</span>
              </div>
              <div class="event-info">
                <h3 class="event-title">
                  <a href="{{ event.url }}">{{ event.title }}</a>
                </h3>
                <p class="event-location">{{ event.location }}</p>
                <p class="event-organizer">{{ event.organizer }}</p>
              </div>
            </div>
            {% endfor %}
          </div>
        </section>
      </div>

      <!-- 右侧边栏 -->
      <div class="content-sidebar">
        <!-- 热门话题 -->
        <div class="sidebar-widget">
          <h3 class="widget-title">热门话题</h3>
          <div class="trending-topics">
            <a href="#" class="topic-tag">#数字营销</a>
            <a href="#" class="topic-tag">#创意设计</a>
            <a href="#" class="topic-tag">#品牌策略</a>
            <a href="#" class="topic-tag">#社交媒体</a>
            <a href="#" class="topic-tag">#广告创意</a>
          </div>
        </div>

        <!-- 最新讨论 -->
        <div class="sidebar-widget">
          <h3 class="widget-title">最新讨论</h3>
          <div class="discussions-list">
            {% for discussion in latest_discussions %}
            <div class="discussion-item">
              <h4 class="discussion-title">
                <a href="#">{{ discussion.title }}</a>
              </h4>
              <div class="discussion-meta">
                <span class="author">{{ discussion.author.username }}</span>
                <span class="replies">{{ discussion.replies_count }} 回复</span>
              </div>
            </div>
            {% endfor %}
          </div>
        </div>

        <!-- 研究报告 -->
        <div class="sidebar-widget">
          <h3 class="widget-title">最新报告</h3>
          <div class="reports-list">
            {% for report in latest_reports %}
            <div class="report-item">
              <h4 class="report-title">
                <a href="{{ report.url }}">{{ report.title }}</a>
              </h4>
              <p class="report-author">{{ report.author }}</p>
              {% if report.is_free %}
              <span class="report-free">免费</span>
              {% endif %}
            </div>
            {% endfor %}
          </div>
        </div>

        <!-- 订阅区域 -->
        <div class="sidebar-widget newsletter-widget">
          <h3 class="widget-title">订阅我们的新闻</h3>
          <p class="widget-description">获取最新的行业新闻和创意灵感</p>
          <form class="newsletter-form">
            <input
              type="email"
              placeholder="输入您的邮箱地址"
              class="newsletter-input"
            />
            <button type="submit" class="newsletter-btn">订阅</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- 底部特色内容 -->
<section class="featured-section">
  <div class="container">
    <h2 class="section-title">精选内容</h2>
    <div class="featured-grid">
      {% for module in modules %} {% if forloop.counter > 1 %}
      <div class="featured-module">
        <h3 class="module-title">{{ module.title }}</h3>
        <div class="module-items">
          {% for item in module.items %}
          <div class="module-item">
            {% if item.hero_image %}
            <div class="item-image">
              {% image item.hero_image fill-200x150 %}
            </div>
            {% endif %}
            <div class="item-content">
              <h4 class="item-title">
                <a href="{{ item.url }}">{{ item.title }}</a>
              </h4>
              <span class="item-date">{{ item.date|date:"M d" }}</span>
            </div>
          </div>
          {% endfor %}
        </div>
      </div>
      {% endif %} {% endfor %}
    </div>
  </div>
</section>
{% endblock %}
```

## 性能优化策略

### 1. 数据库查询优化

```python
# 使用 select_related 减少查询
qs = ArticlePage.objects.live().public().specific().descendant_of(site_root).select_related("hero_image")

# 使用 prefetch_related 优化多对多关系
qs = qs.prefetch_related("channels", "tags")
```

### 2. 缓存策略

```python
# 模板缓存
{% cache 300 "home" request.site.id m.title m.sig %}
<section class="home-module">
    <!-- 内容 -->
</section>
{% endcache %}

# 视图缓存
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 缓存15分钟
def api_home(request):
    # API 逻辑
    pass
```

### 3. 静态文件优化

```python
# 压缩静态文件
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# CDN 配置
STATIC_URL = 'https://cdn.example.com/static/'
```

## 安全考虑

### 1. CSRF 保护

```python
# 所有表单都包含 CSRF 令牌
{% csrf_token %}
```

### 2. XSS 防护

```python
# 使用 safe 过滤器时要谨慎
{{ content|safe }}  # 只在信任的内容上使用

# 使用 escape 过滤器
{{ user_input|escape }}
```

### 3. SQL 注入防护

```python
# 使用 ORM 查询，避免原始 SQL
ArticlePage.objects.filter(title__icontains=search_term)
```

## 测试策略

### 1. 单元测试

```python
from django.test import TestCase
from wagtail.test.utils import WagtailPageTests

class HomePageTests(WagtailPageTests):
    def test_home_page_creation(self):
        # 测试首页创建
        pass

    def test_home_page_context(self):
        # 测试首页上下文数据
        pass
```

### 2. 集成测试

```python
from django.test import Client

class SiteIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
```

## 部署检查清单

### 1. 环境配置

- [ ] DEBUG = False
- [ ] ALLOWED_HOSTS 配置
- [ ] 数据库配置
- [ ] 静态文件配置
- [ ] 媒体文件配置

### 2. 安全配置

- [ ] SECRET_KEY 环境变量
- [ ] HTTPS 配置
- [ ] 安全头部配置
- [ ] 数据库权限配置

### 3. 性能配置

- [ ] 缓存配置
- [ ] 静态文件压缩
- [ ] 数据库连接池
- [ ] 日志配置

## 总结

本项目成功实现了基于 Wagtail CMS 7.1 的 The Drum 风格新闻平台，主要技术成就包括：

1. **完整的多站点管理系统**: 实现了站点级别的内容隔离和权限管理
2. **现代化的前端设计**: 采用 CSS Grid、Flexbox 和现代设计原则
3. **灵活的内容模型**: 支持文章、创意作品、活动、研究报告等多种内容类型
4. **响应式设计**: 完美适配各种设备尺寸
5. **性能优化**: 实现了数据库查询优化、缓存策略和静态文件优化

项目为新闻媒体和内容平台提供了一个完整的解决方案，可以作为同类项目的基础框架进行扩展和定制。

---

**文档版本**: 1.0  
**最后更新**: 2025 年 8 月  
**维护者**: 开发团队
