# The Drum 风格网站实现指南

## 🎯 项目概述

本项目基于 Wagtail CMS 实现了类似 [The Drum](https://web.archive.org/web/20171228015844/http://www.thedrum.com/) 的专业营销、广告和创意行业新闻平台。

## 🚀 快速开始

### 1. 环境准备

确保您已经安装了所有依赖：

```bash
pip install -r requirements.txt
```

### 2. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. 初始化数据

```bash
# 初始化站点设置
python manage.py init_site_settings

# 初始化The Drum风格数据
python manage.py init_thedrum_data
```

### 4. 启动服务器

```bash
python manage.py runserver 0.0.0.0:9000
```

### 5. 访问网站

- **前台**: http://localhost:9000/
- **管理后台**: http://localhost:9000/admin/

## 📋 功能模块

### 1. 内容管理系统

#### 文章管理 (ArticlePage)

- 支持多种内容类型：新闻、分析、观点
- 分类标签系统
- 特色文章标记
- SEO 优化

#### 创意作品 (CreativeWorkPage)

- 代理公司信息
- 客户信息
- 项目简介和成果
- 获奖情况
- 视频链接

#### 行业活动 (IndustryEventPage)

- 活动日期和地点
- 主办方信息
- 活动类型分类
- 报名链接
- 详细议程

#### 研究报告 (ResearchReportPage)

- 报告类型分类
- 作者/机构信息
- 下载链接
- 免费/付费设置
- 关键发现

### 2. 用户系统

#### 用户资料 (UserProfile)

- 公司信息
- 职位信息
- 行业分类
- 个人简介
- 社交媒体链接

#### 贡献者功能

- 贡献者认证
- 专业领域
- 文章统计
- 关注者系统

#### 用户活动

- 活动记录
- 互动统计
- 行为分析

### 3. 社区功能

#### 讨论系统 (Discussion)

- 话题分类
- 标签系统
- 回复功能
- 点赞系统

#### 评论系统 (Comment)

- 通用评论
- 回复功能
- 审核机制

#### 通知系统 (Notification)

- 实时通知
- 多种通知类型
- 已读状态

### 4. 站点设置

#### 主题设置 (SiteTheme)

- 主题样式选择
- 主色调配置
- Logo 和 Favicon
- 自定义 CSS

#### SEO 设置 (SEOSettings)

- 页面标题和描述
- 关键词配置
- 统计代码
- Robots.txt

#### 广告设置 (AdSettings)

- 广告开关
- 广告位配置
- 广告网络选择
- 自定义广告代码

#### 社交媒体设置 (SocialSettings)

- 社交媒体链接
- 联系方式
- 品牌信息

## 🎨 前端设计

### 设计特点

1. **现代化设计**

   - 响应式布局
   - 卡片式设计
   - 渐变色彩
   - 动画效果

2. **用户体验**

   - 直观的导航
   - 快速加载
   - 移动端优化
   - 无障碍设计

3. **内容展示**
   - 英雄区域轮播
   - 分类标签切换
   - 网格布局
   - 侧边栏小工具

### 主要页面

#### 首页 (home_page.html)

- 英雄区域展示特色内容
- 新闻分类标签
- 最新新闻网格
- 创意作品展示
- 即将举行的活动
- 侧边栏小工具

#### 文章页面

- 文章内容展示
- 相关文章推荐
- 评论系统
- 分享功能

#### 创意作品页面

- 作品详情展示
- 代理公司和客户信息
- 项目过程展示
- 相关作品推荐

## 🔧 技术实现

### 后端技术栈

- **Django 5.0** - Web 框架
- **Wagtail 7.1** - CMS 系统
- **SQLite/PostgreSQL** - 数据库
- **Redis** - 缓存系统

### 前端技术栈

- **HTML5/CSS3** - 页面结构和样式
- **JavaScript** - 交互功能
- **React** - 组件化开发
- **HTMX** - 动态内容加载

### 核心功能

#### 多站点支持

```python
# 每个站点独立配置
site = Site.find_for_request(request)
settings = SiteTheme.for_site(site)
```

#### 内容分类

```python
# 频道分类系统
channels = Channel.objects.filter(category_type='news')
```

#### 用户权限

```python
# 贡献者权限控制
if user.profile.is_contributor:
    # 允许发布内容
```

## 📊 数据管理

### 内容创建流程

1. **登录管理后台**
2. **选择内容类型**
3. **填写基本信息**
4. **设置分类标签**
5. **配置 SEO 信息**
6. **发布内容**

### 内容审核

- 自动审核：基础内容检查
- 人工审核：敏感内容审核
- 发布控制：定时发布

### 数据统计

- 访问量统计
- 用户行为分析
- 内容效果评估
- 转化率分析

## 🚀 部署指南

### 开发环境

```bash
# 克隆项目
git clone <repository-url>
cd news-stack

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp env.example .env
# 编辑 .env 文件

# 数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 初始化数据
python manage.py init_site_settings
python manage.py init_thedrum_data

# 启动开发服务器
python manage.py runserver
```

### 生产环境

1. **服务器配置**

   - 使用 Nginx 作为反向代理
   - 配置 SSL 证书
   - 设置静态文件服务

2. **数据库配置**

   - 使用 PostgreSQL
   - 配置数据库连接池
   - 设置定期备份

3. **缓存配置**

   - 使用 Redis 缓存
   - 配置 CDN
   - 优化静态资源

4. **监控配置**
   - 日志监控
   - 性能监控
   - 错误追踪

## 🔍 SEO 优化

### 技术 SEO

- 响应式设计
- 页面加载速度优化
- 结构化数据标记
- XML 站点地图

### 内容 SEO

- 关键词优化
- 内容质量提升
- 内部链接优化
- 外部链接建设

### 本地 SEO

- 地理位置标记
- 本地关键词优化
- 本地目录提交

## 📈 性能优化

### 前端优化

- 图片懒加载
- CSS/JS 压缩
- 浏览器缓存
- CDN 加速

### 后端优化

- 数据库查询优化
- 缓存策略
- 代码优化
- 服务器配置

## 🔒 安全措施

### 数据安全

- 数据加密
- 访问控制
- 备份策略
- 隐私保护

### 应用安全

- SQL 注入防护
- XSS 攻击防护
- CSRF 保护
- 文件上传安全

## 📞 技术支持

### 常见问题

1. **数据库连接问题**

   - 检查数据库配置
   - 确认数据库服务运行
   - 验证连接权限

2. **静态文件问题**

   - 运行 `python manage.py collectstatic`
   - 检查静态文件路径
   - 配置 Web 服务器

3. **权限问题**
   - 检查文件权限
   - 验证用户权限
   - 配置 SELinux

### 联系支持

- 技术文档：查看项目文档
- 问题反馈：提交 Issue
- 功能建议：提交 Feature Request

## 🎯 未来规划

### 功能扩展

- 移动端应用
- 视频内容支持
- 直播功能
- AI 内容推荐

### 技术升级

- 微服务架构
- 容器化部署
- 云原生支持
- 大数据分析

### 业务发展

- 多语言支持
- 国际化部署
- 商业模式优化
- 合作伙伴生态

---

**注意**: 本指南基于当前版本，随着项目发展可能会有所更新。请关注项目文档获取最新信息。
