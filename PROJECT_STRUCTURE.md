# Wagtail 多站点新闻平台项目结构详解

## 项目概述

这是一个基于 Wagtail CMS 的多站点新闻平台，支持多频道、文章管理、首页模块编排、审核工作流等功能。

## 根目录结构

```
news-stack/
├── 📁 venv/                    # Python虚拟环境
├── 📁 news_platform/           # Django主项目配置
├── 📁 news/                    # 新闻应用模块
├── 📁 core/                    # 核心功能模块
├── 📁 authapp/                 # 认证应用模块
├── 📁 portal/                  # 门户API模块
├── 📁 portal_next/             # Next.js前端模块
├── 📁 static/                  # 静态文件
├── 📁 templates/               # Django模板文件
├── 📄 manage.py                # Django管理脚本
├── 📄 requirements.txt         # Python依赖包
├── 📄 README.md               # 项目说明
└── 📄 .env                     # 环境变量配置
```

## 详细目录说明

### 🏗️ 项目配置目录

#### `news_platform/` - Django 主项目

```
news_platform/
├── 📄 __init__.py             # Python包标识
├── 📄 settings.py             # Django项目设置
├── 📄 urls.py                 # 主URL配置
├── 📄 wsgi.py                 # WSGI应用入口
└── 📄 asgi.py                 # ASGI应用入口
```

**作用**：

- **settings.py**: 项目核心配置，包含数据库、缓存、中间件等设置
- **urls.py**: 定义项目的 URL 路由规则
- **wsgi.py/asgi.py**: Web 服务器网关接口

**开发要点**：

- 修改 `settings.py` 添加新的应用和配置
- 在 `urls.py` 中添加新的 URL 路由
- 配置环境变量在 `.env` 文件中

### 📰 新闻应用模块

#### `news/` - 新闻内容管理

```
news/
├── 📄 __init__.py
├── 📄 apps.py                 # 应用配置
├── 📄 models.py               # 数据模型定义
└── 📁 management/
    └── 📁 commands/
        └── 📄 reindex_opensearch.py  # OpenSearch重建索引命令
```

**核心模型**：

- **Channel**: 新闻频道（科技、体育、娱乐等）
- **ArticlePage**: 文章页面模型
- **SectionIndexPage**: 分类索引页面
- **ChannelsIndexPage**: 频道列表页面

**功能特性**：

- 支持多频道分类
- 文章标签系统
- 特色文章标记
- 自动排序和分页
- OpenSearch 全文搜索

**开发要点**：

- 在 `models.py` 中添加新的内容模型
- 使用 `@register_snippet` 注册可重用内容
- 通过 `StreamField` 创建灵活的内容结构

### 🎯 核心功能模块

#### `core/` - 核心功能和首页

```
core/
├── 📄 __init__.py
├── 📄 apps.py
├── 📄 models.py               # 核心数据模型
├── 📄 wagtail_hooks.py        # Wagtail钩子函数
└── 📁 management/
    └── 📁 commands/
        ├── 📄 bootstrap_sites.py    # 初始化站点
        ├── 📄 seed_demo.py          # 创建演示数据
        └── 📄 setup_workflow.py     # 设置工作流
```

**核心模型**：

- **HomePage**: 首页模型，支持模块化内容编排
- **HomeToggles**: 首页设置（全局配置）
- **ChannelModuleBlock**: 频道内容模块
- **FeaturedItem**: 首页精选文章

**功能特性**：

- 首页模块化编排
- 自动内容补齐
- 跨频道内容推荐
- 全局设置管理

**开发要点**：

- 使用 `StreamField` 创建灵活的首页布局
- 通过 `@register_setting` 注册全局设置
- 在 `wagtail_hooks.py` 中添加自定义管理界面功能

### 🔐 认证应用模块

#### `authapp/` - 用户认证和权限

```
authapp/
├── 📄 __init__.py
├── 📄 apps.py
├── 📄 urls.py                 # 认证URL配置
└── 📄 views.py                # 认证视图函数
```

**功能特性**：

- 用户登录/注册
- 权限管理
- OIDC 集成（Logto）
- JWT 令牌处理

**开发要点**：

- 在 `views.py` 中添加自定义认证逻辑
- 配置 OIDC 提供商设置
- 实现自定义权限检查

### 🌐 门户 API 模块

#### `portal/` - API 接口

```
portal/
├── 📄 __init__.py
├── 📄 apps.py
└── 📄 views.py                # API视图函数
```

**功能特性**：

- RESTful API 接口
- 文章数据 API
- 频道数据 API
- 前端数据接口

**开发要点**：

- 使用 Django REST framework 创建 API
- 实现数据序列化
- 添加 API 认证和权限

### ⚛️ Next.js 前端模块

#### `portal_next/` - 现代化前端

```
portal_next/
├── 📄 next.config.js          # Next.js配置
├── 📄 package.json            # Node.js依赖
├── 📄 README.md               # 前端说明
└── 📁 pages/                  # 页面组件
```

**功能特性**：

- SSR/ISR 渲染
- 现代化 UI 组件
- 响应式设计
- 性能优化

**开发要点**：

- 使用 React 组件开发页面
- 配置 SSR/ISR 渲染策略
- 实现前后端数据交互

### 🎨 前端资源目录

#### `static/` - 静态文件

```
static/
├── 📄 react-island.js         # React组件
└── 📄 site.css                # 全局样式
```

**作用**：

- 存放 CSS、JavaScript、图片等静态资源
- 支持 CDN 部署
- 版本控制和缓存

#### `templates/` - Django 模板

```
templates/
├── 📄 base.html               # 基础模板
├── 📁 core/                   # 核心模板
├── 📁 fragments/              # 模板片段
└── 📁 news/                   # 新闻模板
```

**模板结构**：

- **base.html**: 所有页面的基础模板
- **core/**: 首页和核心页面模板
- **news/**: 新闻相关页面模板
- **fragments/**: 可重用的模板片段

## 开发工作流程

### 1. 内容模型开发

```bash
# 在 news/models.py 中添加新模型
# 在 core/models.py 中添加核心功能
# 运行数据库迁移
python manage.py makemigrations
python manage.py migrate
```

### 2. 页面模板开发

```bash
# 在 templates/ 目录下创建模板
# 继承 base.html
# 使用Wagtail模板标签
```

### 3. API 接口开发

```bash
# 在 portal/views.py 中添加API视图
# 配置URL路由
# 测试API接口
```

### 4. 前端组件开发

```bash
# 在 portal_next/ 中开发React组件
# 配置Next.js路由
# 实现数据获取
```

### 5. 样式和交互

```bash
# 在 static/ 中添加CSS/JS
# 在 templates/ 中引用静态文件
# 实现响应式设计
```

## 关键配置文件

### 环境变量 (.env)

```bash
# 数据库配置
DATABASE_URL=postgresql://user:pass@localhost/dbname

# Redis缓存
REDIS_URL=redis://localhost:6379/0

# OpenSearch
OS_ENABLED=1
OS_URL=http://localhost:9200
OS_INDEX=news_articles

# Django设置
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=1
```

### 依赖管理

```bash
# 安装新依赖
pip install package_name

# 更新requirements.txt
pip freeze > requirements.txt

# 安装所有依赖
pip install -r requirements.txt
```

## 部署相关

### 生产环境配置

- 使用 PostgreSQL 数据库
- 配置 Redis 缓存
- 启用 OpenSearch 搜索
- 设置静态文件 CDN
- 配置 SSL 证书

### 容器化部署

- 使用 Docker 容器
- 配置 Nginx 反向代理
- 实现负载均衡
- 监控和日志收集

## 扩展开发建议

### 1. 添加新功能模块

```bash
# 创建新的Django应用
python manage.py startapp new_module

# 在settings.py中注册应用
INSTALLED_APPS = [
    ...
    "new_module",
]
```

### 2. 自定义 Wagtail 功能

```bash
# 在wagtail_hooks.py中添加钩子
# 自定义管理界面
# 添加自定义块类型
```

### 3. 性能优化

```bash
# 数据库查询优化
# 缓存策略
# 静态文件优化
# CDN配置
```

### 4. 测试和调试

```bash
# 单元测试
python manage.py test

# 功能测试
pytest

# 性能测试
# 使用django-silk等工具
```

这个项目结构设计合理，支持多站点、模块化开发，适合团队协作和持续开发。每个目录都有明确的职责，便于维护和扩展。
