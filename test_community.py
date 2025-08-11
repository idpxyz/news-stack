#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_platform.settings')
django.setup()

from community.models import Discussion, Comment, Like, Tag
from django.contrib.auth.models import User

def test_community():
    """测试社区功能"""
    print("测试社区功能...")
    
    # 检查模型是否存在
    print(f"Discussion 模型: {Discussion}")
    print(f"Comment 模型: {Comment}")
    print(f"Like 模型: {Like}")
    print(f"Tag 模型: {Tag}")
    
    # 检查数据库表
    try:
        discussions = Discussion.objects.all()
        print(f"现有讨论数量: {discussions.count()}")
        
        comments = Comment.objects.all()
        print(f"现有评论数量: {comments.count()}")
        
        likes = Like.objects.all()
        print(f"现有点赞数量: {likes.count()}")
        
        tags = Tag.objects.all()
        print(f"现有标签数量: {tags.count()}")
        
        users = User.objects.all()
        print(f"现有用户数量: {users.count()}")
        
        print("✅ 社区功能测试通过！")
        
    except Exception as e:
        print(f"❌ 社区功能测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_community() 