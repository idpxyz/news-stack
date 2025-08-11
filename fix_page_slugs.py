#!/usr/bin/env python
import os
import sys
import django
import re
from django.utils.text import slugify

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_platform.settings')
django.setup()

from news.models import ArticlePage, CreativeWorkPage, IndustryEventPage, ResearchReportPage

def contains_chinese(text):
    """检查文本是否包含中文字符"""
    if not text:
        return False
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    return bool(chinese_pattern.search(text))

def generate_english_slug(title, page_id):
    """从标题生成英文slug"""
    if not title:
        return f"page-{page_id}"
    
    # 移除特殊字符，只保留字母、数字、空格
    clean_title = re.sub(r'[^\w\s-]', '', title)
    
    # 转换为小写并替换空格为连字符
    slug = slugify(clean_title)
    
    # 如果slug为空或太短，使用默认值
    if not slug or len(slug) < 3:
        slug = f"page-{page_id}"
    
    return slug

def fix_page_slugs():
    """修复所有页面的slug"""
    page_models = [ArticlePage, CreativeWorkPage, IndustryEventPage, ResearchReportPage]
    
    for model in page_models:
        print(f'\n处理 {model.__name__} 页面...')
        
        pages = model.objects.all()
        for page in pages:
            old_slug = page.slug
            
            # 检查slug是否包含中文
            if contains_chinese(old_slug):
                # 生成新的英文slug
                new_slug = generate_english_slug(page.title, page.id)
                
                print(f'  {page.title}')
                print(f'    旧slug: {old_slug}')
                print(f'    新slug: {new_slug}')
                
                # 检查新slug是否已存在
                existing_page = model.objects.filter(slug=new_slug).exclude(id=page.id).first()
                if existing_page:
                    new_slug = f"{new_slug}-{page.id}"
                    print(f'    调整slug: {new_slug} (避免冲突)')
                
                page.slug = new_slug
                page.save()
                print(f'    ✓ 已更新')
            else:
                print(f'  {page.title} - slug已经是英文: {old_slug}')
    
    print('\n所有页面slug修复完成！')

if __name__ == '__main__':
    fix_page_slugs() 