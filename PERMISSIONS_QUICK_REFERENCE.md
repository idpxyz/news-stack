# Wagtail 多站点权限管理快速参考

## 🎯 权限管理核心概念

### 权限层次结构

1. **超级用户**: 拥有所有权限
2. **全局权限**: 通过 `is_staff` 和全局权限分配
3. **站点特定权限**: 通过 `GroupSitePermission` 分配
4. **页面级权限**: 通过 `GroupPagePermission` 分配

### 关键问题回答

**Q: 不同的站点管理员只能管理自己的站点吗？**

**A: 是的，通过站点特定权限可以实现站点隔离管理。**

- ✅ **站点隔离**: 每个站点管理员只能管理自己站点的内容
- ✅ **权限细分**: 可以为不同角色分配不同权限级别
- ✅ **灵活配置**: 支持一个用户管理多个站点
- ✅ **安全控制**: 防止跨站点未授权访问

## 🚀 快速开始

### 1. 设置权限结构

```bash
# 为所有站点创建权限组
python manage.py setup_site_permissions
```

### 2. 创建站点管理员

```bash
# 创建用户
python manage.py createsuperuser --username newsadmin --email news@example.com

# 分配站点权限
python manage.py setup_site_permissions --site news.local --user newsadmin --role admin
```

### 3. 验证权限

```bash
# 查看所有用户权限
python manage.py setup_site_permissions --list-users
```

## 👥 角色权限对照表

| 角色          | 添加页面 | 编辑页面 | 删除页面 | 发布页面 | 管理站点 | 管理集合 |
| ------------- | -------- | -------- | -------- | -------- | -------- | -------- |
| **admin**     | ✅       | ✅       | ✅       | ✅       | ✅       | ✅       |
| **editor**    | ✅       | ✅       | ❌       | ✅       | ❌       | ❌       |
| **publisher** | ❌       | ✅       | ❌       | ✅       | ❌       | ❌       |
| **moderator** | ❌       | ✅       | ❌       | ✅       | ❌       | ❌       |

## 🔧 常用命令

### 查看信息

```bash
# 查看所有站点
python manage.py setup_site_permissions --list-sites

# 查看所有用户权限
python manage.py setup_site_permissions --list-users
```

### 分配权限

```bash
# 分配管理员权限
python manage.py setup_site_permissions --site <hostname> --user <username> --role admin

# 分配编辑权限
python manage.py setup_site_permissions --site <hostname> --user <username> --role editor

# 分配发布权限
python manage.py setup_site_permissions --site <hostname> --user <username> --role publisher
```

### 创建站点

```bash
# 创建新站点
python manage.py create_site <hostname> "<site_name>" --create-content

# 示例
python manage.py create_site news.local "新闻站点" --create-content
python manage.py create_site sports.local "体育站点" --create-content
```

## 📋 权限管理流程

### 典型工作流程

1. **创建站点** → `create_site`
2. **设置权限结构** → `setup_site_permissions`
3. **创建用户** → `createsuperuser`
4. **分配权限** → `setup_site_permissions --site --user --role`
5. **验证权限** → `setup_site_permissions --list-users`

### 多站点用户管理示例

```bash
# 场景：一个用户管理多个站点
python manage.py createsuperuser --username multieditor --email editor@example.com

# 分配多个站点权限
python manage.py setup_site_permissions --site news.local --user multieditor --role editor
python manage.py setup_site_permissions --site sports.local --user multieditor --role editor
python manage.py setup_site_permissions --site tech.local --user multieditor --role publisher
```

## 🔍 权限验证

### 在管理后台验证

1. 使用分配了权限的用户登录
2. 检查是否只能看到指定站点的内容
3. 验证操作权限是否正确

### 在代码中验证

```python
# Django shell 验证
python manage.py shell

>>> from django.contrib.auth import get_user_model
>>> from wagtail.models import Site, GroupSitePermission
>>>
>>> User = get_user_model()
>>> user = User.objects.get(username='newsadmin')
>>> site = Site.objects.get(hostname='news.local')
>>>
>>> # 检查站点权限
>>> permissions = GroupSitePermission.objects.filter(
...     group__user=user, site=site
... )
>>> print(f"User has {permissions.count()} permissions for {site.hostname}")
```

## ⚠️ 常见问题

### 用户无法访问管理后台

```bash
# 解决方案：设置为staff用户
python manage.py shell
>>> user = User.objects.get(username='username')
>>> user.is_staff = True
>>> user.save()
```

### 权限不生效

```python
# 解决方案：清除缓存并重新登录
from django.core.cache import cache
cache.clear()
# 然后在管理后台重新登录
```

### 用户看不到站点内容

```bash
# 解决方案：检查并重新分配权限
python manage.py setup_site_permissions --list-users
python manage.py setup_site_permissions --site site.local --user username --role editor
```

## 🎯 最佳实践

### 权限设计原则

1. **最小权限**: 只分配工作必需的最小权限
2. **角色分离**: 为不同角色创建不同权限组
3. **定期审查**: 定期检查和更新用户权限
4. **权限文档**: 记录每个角色的权限范围

### 安全建议

- 定期审查用户权限
- 使用强密码策略
- 启用双因素认证（如果支持）
- 记录权限变更日志

## 📚 相关文档

- [多站点操作指南](MULTISITE_GUIDE.md)
- [开发指导](DEVELOPMENT_GUIDE.md)
- [项目结构详解](PROJECT_STRUCTURE.md)

---

**快速测试**: 运行 `python manage.py setup_site_permissions --list-users` 查看当前权限状态。
