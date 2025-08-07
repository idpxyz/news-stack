# Wagtail 多站点新闻平台

一个基于 Wagtail CMS 的现代化多站点新闻平台，支持多频道、文章管理、首页模块编排、审核工作流等功能。

## 🎯 项目特性

- **多站点支持**: 可管理多个独立的新闻站点
- **25 个中文频道**: 参考今日头条的频道分类
- **模块化首页**: 灵活的首页内容编排
- **API 优先设计**: 支持前后端分离
- **现代化技术栈**: Wagtail + Django + Next.js
- **权限管理**: 站点隔离的权限控制系统
- **工作流支持**: 完整的审核和发布流程

## 🚀 快速开始

### 环境要求

- Python 3.8+ (推荐 3.12)
- Node.js 16+ (用于 Next.js 前端)
- Git

### 安装步骤

1. **克隆项目**

```bash
git clone <your-repository-url>
cd news-stack
```

2. **设置虚拟环境**

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
.\venv\Scripts\Activate.ps1

# 激活虚拟环境 (Linux/Mac)
source venv/bin/activate
```

3. **安装依赖**

```bash
# 升级pip
python -m pip install --upgrade pip

# 安装Python依赖
pip install -r requirements.txt
```

4. **环境配置**

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑环境变量
# 根据需要修改 .env 文件
```

5. **数据库初始化**

```bash
# 创建数据库迁移
python manage.py makemigrations

# 应用迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

6. **生成演示数据**

```bash
# 初始化站点
python manage.py bootstrap_sites

# 生成演示数据
python manage.py seed_demo

# 设置工作流
python manage.py setup_workflow

# 设置权限结构
python manage.py setup_site_permissions
```

7. **启动开发服务器**

```bash
# 启动Django服务器
python manage.py runserver 0.0.0.0:9000

# 访问地址
# 前台: http://localhost:9000/
# 管理后台: http://localhost:9000/admin/
```

## 📚 文档

- [开发指导](DEVELOPMENT_GUIDE.md) - 完整的开发、测试和部署指南
- [多站点操作指南](MULTISITE_GUIDE.md) - 多站点创建和管理
- [权限管理快速参考](PERMISSIONS_QUICK_REFERENCE.md) - 权限配置和用户管理
- [项目结构详解](PROJECT_STRUCTURE.md) - 项目目录结构说明
- [包管理指南](PACKAGE_MANAGEMENT.md) - Python 包管理最佳实践
- [虚拟环境设置](VENV_SETUP.md) - 虚拟环境配置指南

## 🔧 管理命令

### 站点管理

```bash
# 创建新站点
python manage.py create_site news.local "新闻站点" --create-content

# 查看所有站点
python manage.py setup_site_permissions --list-sites
```

### 权限管理

```bash
# 设置权限结构
python manage.py setup_site_permissions

# 分配用户权限
python manage.py setup_site_permissions --site news.local --user username --role admin

# 查看用户权限
python manage.py setup_site_permissions --list-users
```

### 数据管理

```bash
# 生成演示数据
python manage.py seed_demo

# 重建搜索索引
python manage.py reindex_opensearch
```

## 🌐 多站点访问

配置 hosts 文件后，可以访问不同的站点：

```
http://news.local:9000/      # 新闻站点
http://sports.local:9000/    # 体育站点
http://tech.local:9000/      # 科技站点
http://localhost:9000/admin/ # 管理后台
```

## 🏗️ 技术架构

- **后端**: Django 5.0 + Wagtail 7.1
- **前端**: Next.js (SSR/ISR)
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **缓存**: Redis
- **搜索**: OpenSearch (可选)
- **认证**: Logto OIDC

## 🤝 贡献

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持

- 项目 Issues: [GitHub Issues](https://github.com/your-repo/issues)
- 技术讨论: [GitHub Discussions](https://github.com/your-repo/discussions)

---

**注意**: 这是一个开发中的项目，生产环境使用前请仔细测试。
