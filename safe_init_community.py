#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_platform.settings')
django.setup()

from community.models import Discussion, Comment, Like, Tag
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta

def safe_init_community():
    """安全地初始化社区数据"""
    print("开始安全初始化社区数据...")
    
    # 创建测试用户
    user1, created = User.objects.get_or_create(
        username='marketer001',
        defaults={
            'email': 'marketer001@example.com',
            'password': 'password123',
            'first_name': '张',
            'last_name': '营销'
        }
    )
    if created:
        user1.set_password('password123')
        user1.save()
        print(f'创建用户: {user1.username}')
    else:
        print(f'用户已存在: {user1.username}')
    
    user2, created = User.objects.get_or_create(
        username='designer001',
        defaults={
            'email': 'designer001@example.com',
            'password': 'password123',
            'first_name': '李',
            'last_name': '设计'
        }
    )
    if created:
        user2.set_password('password123')
        user2.save()
        print(f'创建用户: {user2.username}')
    else:
        print(f'用户已存在: {user2.username}')
    
    # 创建标签（处理slug冲突）
    tags_data = [
        '数字营销', '创意设计', '品牌策略', '社交媒体', '广告创意',
        '用户体验', '数据分析', '内容营销', 'SEO优化', '品牌建设'
    ]
    
    tags = {}
    for tag_name in tags_data:
        base_slug = slugify(tag_name)
        slug = base_slug
        counter = 1
        
        # 处理slug冲突
        while Tag.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        tag, created = Tag.objects.get_or_create(
            name=tag_name,
            defaults={'slug': slug}
        )
        tags[tag_name] = tag
        if created:
            print(f'创建标签: {tag_name} (slug: {slug})')
        else:
            print(f'标签已存在: {tag_name}')
    
    # 创建讨论
    discussions_data = [
        {
            'title': '2024年数字营销趋势分析',
            'content': '''大家好！想和大家分享一下我对2024年数字营销趋势的看法。

**主要趋势：**
1. AI驱动的个性化营销
2. 短视频内容营销
3. 私域流量运营
4. 数据隐私保护

大家觉得哪些趋势最值得关注？有什么实践经验可以分享吗？''',
            'author': user1,
            'tags': ['数字营销', '数据分析', '内容营销']
        },
        {
            'title': '如何提升品牌设计的视觉冲击力？',
            'content': '''作为一名设计师，我一直在思考如何让品牌设计更有视觉冲击力。

**我的思考：**
- 色彩搭配的重要性
- 字体选择的艺术
- 图形元素的运用
- 品牌一致性的维护

想听听大家的想法和建议！''',
            'author': user2,
            'tags': ['创意设计', '品牌策略', '用户体验']
        },
        {
            'title': '社交媒体营销效果如何量化？',
            'content': '''在做社交媒体营销时，我们经常面临效果量化的问题。

**关键指标：**
- 粉丝增长率
- 互动率
- 转化率
- ROI

大家有什么好的量化方法和工具推荐吗？''',
            'author': user1,
            'tags': ['社交媒体', '数据分析', '数字营销']
        }
    ]
    
    for i, discussion_data in enumerate(discussions_data):
        discussion, created = Discussion.objects.get_or_create(
            title=discussion_data['title'],
            defaults={
                'content': discussion_data['content'],
                'author': discussion_data['author'],
                'created_at': timezone.now() - timedelta(days=i*2)
            }
        )
        
        if created:
            print(f'创建讨论: {discussion.title}')
            
            # 添加标签（在创建Discussion之后）
            for tag_name in discussion_data['tags']:
                if tag_name in tags:
                    discussion.tags.add(tags[tag_name])
            
            # 为每个讨论添加一些评论
            comments_data = [
                {
                    'content': '非常详细的趋势分析，AI营销确实是未来的重点！',
                    'author': user2
                },
                {
                    'content': '同意楼主的观点，短视频营销现在确实很火。',
                    'author': user1
                }
            ]
            
            for j, comment_data in enumerate(comments_data):
                comment = Comment.objects.create(
                    discussion=discussion,
                    content=comment_data['content'],
                    author=comment_data['author'],
                    created_at=discussion.created_at + timedelta(hours=j+1)
                )
                print(f'  添加评论: {comment.content[:30]}...')
            
            # 添加一些点赞
            if i % 2 == 0:
                Like.objects.create(discussion=discussion, user=user2)
            if i % 3 == 0:
                Like.objects.create(discussion=discussion, user=user1)
        else:
            print(f'讨论已存在: {discussion.title}')
    
    print('\n社区数据初始化完成！')
    print(f'总计: {Discussion.objects.count()} 个讨论')
    print(f'总计: {Comment.objects.count()} 条评论')
    print(f'总计: {Like.objects.count()} 个点赞')
    print(f'总计: {Tag.objects.count()} 个标签')

if __name__ == '__main__':
    safe_init_community() 