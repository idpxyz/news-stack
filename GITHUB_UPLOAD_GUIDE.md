# GitHub 上传指南

本指南将帮助您将 Wagtail 多站点新闻平台项目上传到 GitHub。

## 🎯 准备工作

### 1. 确保项目完整性

在上传前，请确保以下文件已准备就绪：

- ✅ `.gitignore` - 排除不需要的文件
- ✅ `README.md` - 项目说明文档
- ✅ `LICENSE` - 许可证文件
- ✅ `requirements.txt` - Python 依赖
- ✅ `env.example` - 环境变量模板
- ✅ 所有项目文档

### 2. 检查敏感信息

确保以下敏感信息不会被上传：

- ❌ 数据库文件 (`db.sqlite3`)
- ❌ 虚拟环境目录 (`venv/`)
- ❌ 环境变量文件 (`.env`)
- ❌ 日志文件 (`*.log`)
- ❌ 媒体文件 (`media/`)
- ❌ 静态文件收集目录 (`staticfiles/`)

## 🚀 上传步骤

### 方法一：使用 GitHub Desktop (推荐新手)

#### 1. 安装 GitHub Desktop

- 访问 [GitHub Desktop](https://desktop.github.com/) 下载安装

#### 2. 登录 GitHub 账户

- 打开 GitHub Desktop
- 使用 GitHub 账户登录

#### 3. 创建新仓库

```bash
# 在 GitHub Desktop 中
1. 点击 "File" → "New Repository"
2. 填写仓库信息：
   - Name: wagtail-multisite-news
   - Description: Wagtail 多站点新闻平台
   - Local path: 选择项目目录
   - 勾选 "Initialize this repository with a README"
3. 点击 "Create Repository"
```

#### 4. 添加文件并提交

```bash
# 在 GitHub Desktop 中
1. 查看 "Changes" 标签页
2. 选择要提交的文件
3. 填写提交信息：
   - Summary: "Initial commit: Wagtail multi-site news platform"
   - Description: 详细描述项目特性
4. 点击 "Commit to main"
```

#### 5. 推送到 GitHub

```bash
# 在 GitHub Desktop 中
1. 点击 "Push origin"
2. 等待上传完成
```

### 方法二：使用命令行 (推荐开发者)

#### 1. 初始化 Git 仓库

```bash
# 在项目根目录执行
git init
```

#### 2. 添加远程仓库

```bash
# 替换为您的 GitHub 仓库 URL
git remote add origin https://github.com/your-username/wagtail-multisite-news.git
```

#### 3. 添加文件到暂存区

```bash
# 添加所有文件（除了 .gitignore 中排除的）
git add .

# 检查暂存区状态
git status
```

#### 4. 提交更改

```bash
# 创建初始提交
git commit -m "Initial commit: Wagtail multi-site news platform

- 多站点支持
- 25个中文频道
- 权限管理系统
- 完整的开发文档
- 管理命令工具"
```

#### 5. 推送到 GitHub

```bash
# 推送到主分支
git push -u origin main

# 如果使用 master 分支
git push -u origin master
```

## 📋 上传检查清单

### 必需文件

- [ ] `.gitignore`
- [ ] `README.md`
- [ ] `LICENSE`
- [ ] `requirements.txt`
- [ ] `env.example`
- [ ] `manage.py`
- [ ] 所有 Python 源代码文件
- [ ] 所有模板文件
- [ ] 所有静态文件
- [ ] 所有文档文件

### 文档文件

- [ ] `DEVELOPMENT_GUIDE.md`
- [ ] `MULTISITE_GUIDE.md`
- [ ] `PERMISSIONS_QUICK_REFERENCE.md`
- [ ] `PROJECT_STRUCTURE.md`
- [ ] `PACKAGE_MANAGEMENT.md`
- [ ] `VENV_SETUP.md`
- [ ] `SETUP_COMPLETE.md`

### 排除文件

- [ ] `db.sqlite3`
- [ ] `venv/` 目录
- [ ] `.env` 文件
- [ ] `__pycache__/` 目录
- [ ] `*.pyc` 文件
- [ ] `media/` 目录
- [ ] `staticfiles/` 目录

## 🔧 高级配置

### 1. 设置 Git 用户信息

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

### 2. 创建 .gitattributes 文件

```bash
# 创建 .gitattributes 文件
echo "*.md text eol=lf" > .gitattributes
echo "*.py text eol=lf" >> .gitattributes
echo "*.js text eol=lf" >> .gitattributes
echo "*.css text eol=lf" >> .gitattributes
echo "*.html text eol=lf" >> .gitattributes
```

### 3. 设置分支保护

在 GitHub 仓库设置中：

1. 进入 "Settings" → "Branches"
2. 添加分支保护规则
3. 启用 "Require pull request reviews"
4. 启用 "Require status checks to pass"

## 📝 仓库描述

### 仓库名称建议

- `wagtail-multisite-news`
- `wagtail-news-platform`
- `multisite-news-cms`

### 标签建议

```
wagtail
django
multisite
cms
news
python
nextjs
permissions
```

### 描述模板

```
Wagtail 多站点新闻平台

基于 Wagtail CMS 的现代化多站点新闻平台，支持：
- 多站点管理
- 25个中文频道
- 权限隔离
- API优先设计
- Next.js前端

技术栈：Django 5.0 + Wagtail 7.1 + Next.js
```

## 🚀 后续步骤

### 1. 设置 GitHub Pages (可选)

```bash
# 在仓库设置中启用 GitHub Pages
# Settings → Pages → Source: Deploy from a branch
# Branch: main, folder: /docs
```

### 2. 创建 Issues 模板

```bash
# 创建 .github/ISSUE_TEMPLATE/bug_report.md
# 创建 .github/ISSUE_TEMPLATE/feature_request.md
```

### 3. 设置 Actions (可选)

```bash
# 创建 .github/workflows/ci.yml
# 配置自动化测试和部署
```

### 4. 添加项目徽章

在 README.md 中添加：

```markdown
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://djangoproject.com)
[![Wagtail](https://img.shields.io/badge/Wagtail-7.1-red.svg)](https://wagtail.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
```

## ❓ 常见问题

### Q: 上传时遇到大文件错误

```bash
# 解决方案：使用 Git LFS
git lfs install
git lfs track "*.sqlite3"
git lfs track "media/**"
```

### Q: 如何更新已上传的项目

```bash
# 修改文件后
git add .
git commit -m "Update: 描述更改内容"
git push origin main
```

### Q: 如何邀请协作者

1. 进入 GitHub 仓库页面
2. 点击 "Settings" → "Collaborators"
3. 点击 "Add people"
4. 输入用户名或邮箱

### Q: 如何创建发布版本

1. 在 GitHub 仓库页面点击 "Releases"
2. 点击 "Create a new release"
3. 填写版本号和描述
4. 上传发布文件

## 🎉 完成

上传完成后，您的项目将可以在 GitHub 上访问，其他开发者可以：

1. **克隆项目**: `git clone https://github.com/your-username/wagtail-multisite-news.git`
2. **查看文档**: 阅读 README.md 和各个指南文档
3. **提交 Issues**: 报告问题或提出建议
4. **贡献代码**: 通过 Pull Request 贡献代码

---

**提示**: 记得定期更新项目文档和依赖，保持项目的活跃度！
