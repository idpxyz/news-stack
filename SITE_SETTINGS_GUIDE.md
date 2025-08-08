# 站点设置功能使用指南

## 🎯 功能概述

本功能通过 Wagtail 的 `@register_setting` 装饰器实现了完整的站点设置系统，支持多站点独立配置：

- **UI主题设置** - 主题样式、主色调、Logo、Favicon、自定义CSS
- **SEO设置** - 页面标题、描述、关键词、统计代码、Robots.txt
- **广告设置** - 广告开关、广告位配置、广告网络选择
- **社交媒体设置** - 微信、微博、抖音、B站、联系方式

## 🚀 快速开始

### 1. 初始化设置

```bash
python manage.py init_site_settings
```

### 2. 访问管理后台

访问 `http://localhost:9000/admin/settings/` 查看所有设置项。

### 3. 配置站点设置

在管理后台的 **Settings** 菜单中，您会看到以下设置项：

- **首页设置** - 内容展示配置
- **站点主题** - UI主题和品牌配置  
- **SEO设置** - 搜索引擎优化
- **广告设置** - 广告投放配置
- **社交媒体设置** - 社交媒体链接

## 📋 详细配置说明

### 🎨 站点主题设置

#### 主题样式
- `default` - 默认主题
- `dark` - 深色主题
- `light` - 浅色主题
- `news` - 新闻主题
- `tech` - 科技主题

#### 主色调
支持十六进制颜色值，如 `#007bff`

#### Logo和Favicon
- Logo地址：站点Logo的URL地址
- Favicon地址：浏览器标签页图标地址

#### 自定义CSS
可以添加额外的CSS样式代码，支持：
- 主题定制
- 品牌色彩
- 特殊样式

### 🔍 SEO设置

#### 基础SEO
- **默认标题**：站点默认的页面标题（60字符以内）
- **默认描述**：站点默认的页面描述（160字符以内）
- **默认关键词**：站点默认的关键词，用逗号分隔

#### 统计代码
- **Google Analytics ID**：GA4的测量ID，如 `G-XXXXXXXXXX`
- **百度统计ID**：百度统计的代码ID

#### Robots.txt
可以自定义robots.txt内容

### 📢 广告设置

#### 广告开关
- **启用广告**：是否在站点显示广告
- **广告网络**：Google AdSense、百度联盟、腾讯广告、自定义

#### 广告位配置
- **头部广告位ID**：页面头部广告位的ID
- **侧边栏广告位ID**：侧边栏广告位的ID
- **底部广告位ID**：页面底部广告位的ID
- **文章内广告位ID**：文章内容中广告位的ID

#### 自定义广告代码
可以添加自定义的广告代码（HTML/JavaScript）

### 📱 社交媒体设置

#### 社交媒体链接
- **微信二维码**：微信公众号二维码图片地址
- **微博地址**：官方微博主页地址
- **抖音地址**：官方抖音主页地址
- **B站地址**：官方B站主页地址

#### 联系方式
- **联系邮箱**：官方联系邮箱
- **联系电话**：官方联系电话

## 🛠️ 在模板中使用

### 加载模板标签

```html
{% load site_settings %}
```

### 获取主题设置

```html
<!-- 获取主题CSS类 -->
<html lang="zh" {% get_theme_css_class %}>

<!-- 获取主色调 -->
{% get_primary_color as primary_color %}

<!-- 获取Logo -->
{% get_logo_url as logo_url %}
{% if logo_url %}
<img src="{{ logo_url }}" alt="Logo">
{% endif %}

<!-- 获取自定义CSS -->
{% get_custom_css as custom_css %}
{% if custom_css %}
<style>{{ custom_css|safe }}</style>
{% endif %}
```

### 获取SEO设置

```html
<!-- 获取SEO设置 -->
{% get_seo_settings as seo_settings %}
<title>{{ page.title }} - {{ seo_settings.meta_title }}</title>
<meta name="description" content="{{ seo_settings.meta_description }}">

<!-- 获取统计代码 -->
{% get_google_analytics_id as ga_id %}
{% if ga_id %}
<!-- Google Analytics 代码 -->
{% endif %}
```

### 获取广告设置

```html
<!-- 检查是否启用广告 -->
{% is_ad_enabled as ads_enabled %}
{% if ads_enabled %}
<!-- 获取广告位ID -->
{% get_ad_slot 'header' as header_ad_slot %}
<div class="ad-slot" data-slot="{{ header_ad_slot }}"></div>
{% endif %}
```

### 获取社交媒体设置

```html
<!-- 获取联系方式 -->
{% get_contact_email as contact_email %}
{% get_contact_phone as contact_phone %}

<!-- 获取社交媒体链接 -->
{% get_weibo_url as weibo_url %}
{% get_wechat_qr as wechat_qr %}
```

## 🔧 技术实现

### 模型结构

所有设置都继承自 `BaseSiteSetting`，支持多站点：

```python
@register_setting
class SiteTheme(BaseSiteSetting):
    theme = models.CharField(choices=THEME_CHOICES, default="default")
    primary_color = models.CharField(default="#007bff")
    # ... 其他字段
```

### 模板标签

提供了丰富的模板标签来获取设置：

- `get_site_theme` - 获取主题设置
- `get_seo_settings` - 获取SEO设置
- `get_ad_settings` - 获取广告设置
- `get_social_settings` - 获取社交媒体设置
- `get_theme_css_class` - 获取主题CSS类
- `is_ad_enabled` - 检查广告是否启用
- `get_ad_slot` - 获取广告位ID

### 管理界面

使用 `MultiFieldPanel` 组织设置界面：

```python
panels = [
    MultiFieldPanel([
        FieldPanel("theme"),
        FieldPanel("primary_color"),
    ], heading="主题配置"),
    # ... 其他面板
]
```

## 🌐 多站点支持

每个站点都有独立的设置：

1. **站点A** 可以配置深色主题 + Google广告
2. **站点B** 可以配置浅色主题 + 百度广告
3. **站点C** 可以配置新闻主题 + 无广告

设置会自动根据当前请求的站点进行切换。

## 📝 最佳实践

### 1. 设置默认值
所有设置都有合理的默认值，确保站点正常运行。

### 2. 渐进式配置
可以先配置基础设置，再逐步完善高级功能。

### 3. 测试验证
配置后及时测试效果，特别是：
- 主题切换
- 广告显示
- 统计代码
- SEO效果

### 4. 备份设置
重要配置建议定期备份。

## 🚨 注意事项

1. **权限控制**：只有超级用户和具有相应权限的用户才能修改设置
2. **缓存影响**：修改设置后可能需要清除缓存
3. **多站点隔离**：确保不同站点的设置不会相互影响
4. **广告合规**：确保广告配置符合相关法规要求

## 📞 技术支持

如果遇到问题，请检查：

1. 数据库迁移是否完成
2. 模板标签是否正确加载
3. 站点设置是否已初始化
4. 权限配置是否正确 