# Wagtail 项目虚拟环境设置指南

## 虚拟环境已创建完成！

✅ 虚拟环境已创建在 `venv/` 目录下  
✅ 所有依赖包已安装完成  
✅ 环境已激活并准备就绪

## 快速激活方法

### Windows PowerShell (推荐)

```powershell
.\activate_venv.ps1
```

### Windows 命令提示符

```cmd
activate_venv.bat
```

### 手动激活

```powershell
# PowerShell
.\venv\Scripts\Activate.ps1

# 命令提示符
venv\Scripts\activate.bat
```

## 验证环境

激活后，命令行前面会显示 `(venv)`，表示虚拟环境已激活：

```powershell
(venv) PS D:\idpxyz\news-stack>
```

## 常用命令

```bash
# 运行开发服务器
python manage.py runserver 0.0.0.0:8000

# 数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 安装新的依赖包
pip install package_name

# 查看已安装的包
pip list

# 退出虚拟环境
deactivate
```

## 项目依赖

主要依赖包包括：

- Django 5.0.14
- Wagtail 7.1
- PostgreSQL (psycopg2-binary)
- Redis (django-redis)
- JWT (PyJWT)
- 其他 Wagtail 相关依赖

## 注意事项

1. **每次开发前都要激活虚拟环境**
2. **不要删除 `venv/` 目录**
3. **新增依赖包后记得更新 `requirements.txt`**
4. **团队协作时，所有成员都应使用相同的虚拟环境**

## 更新依赖

如果 `requirements.txt` 有更新：

```bash
pip install -r requirements.txt --upgrade
```

## 重新创建虚拟环境

如果虚拟环境出现问题，可以重新创建：

```bash
# 删除旧的虚拟环境
rmdir /s venv

# 重新创建
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
