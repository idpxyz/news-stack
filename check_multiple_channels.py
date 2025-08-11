#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_platform.settings')
django.setup()

from wagtail.models import Page
from news.models import ChannelsIndexPage

def check_multiple_channels():
    """检查是否有多个channels页面"""
    print("检查是否有多个channels页面...")
    
    # 查找所有channels页面
    all_channels = ChannelsIndexPage.objects.all()
    print(f"找到 {all_channels.count()} 个ChannelsIndexPage")
    
    for i, page in enumerate(all_channels):
        print(f"\n页面 {i+1}:")
        print(f"  标题: {page.title}")
        print(f"  Slug: {page.slug}")
        print(f"  URL路径: {page.url_path}")
        print(f"  父页面: {page.get_parent().title}")
        print(f"  是否发布: {page.live}")
        print(f"  ID: {page.id}")
    
    # 查找所有slug为channels的页面
    all_channels_by_slug = Page.objects.filter(slug='channels')
    print(f"\n找到 {all_channels_by_slug.count()} 个slug为channels的页面")
    
    for i, page in enumerate(all_channels_by_slug):
        print(f"\n页面 {i+1}:")
        print(f"  标题: {page.title}")
        print(f"  类型: {page.content_type.model}")
        print(f"  URL路径: {page.url_path}")
        print(f"  父页面: {page.get_parent().title}")
        print(f"  是否发布: {page.live}")
        print(f"  ID: {page.id}")
    
    # 检查URL路径
    print(f"\nURL路径检查:")
    urls = ['/channels/', '/media-one/channels/']
    for url in urls:
        try:
            found_page = Page.objects.get(url_path=url.strip('/'))
            print(f"  {url}: 找到页面 {found_page.title} (ID: {found_page.id})")
        except Page.DoesNotExist:
            print(f"  {url}: 未找到页面")
        except Exception as e:
            print(f"  {url}: 错误 - {e}")

if __name__ == '__main__':
    check_multiple_channels()
