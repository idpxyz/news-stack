from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from community.models import Discussion, Comment, Like, Tag
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta

class Command(BaseCommand):
    help = '初始化社区讨论数据'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化社区数据...')
        
        # 创建测试用户
        user1, created = User.objects.get_or_create(
            username='marketer001',
            defaults={
                'email': 'marketer001@example.com',
                'first_name': '张',
                'last_name': '营销'
            }
        )
        if created:
            user1.set_password('password123')
            user1.save()
            self.stdout.write(f'创建用户: {user1.username}')
        
        user2, created = User.objects.get_or_create(
            username='designer001',
            defaults={
                'email': 'designer001@example.com',
                'first_name': '李',
                'last_name': '设计'
            }
        )
        if created:
            user2.set_password('password123')
            user2.save()
            self.stdout.write(f'创建用户: {user2.username}')
        
        # 创建标签
        tags_data = [
            '数字营销', '创意设计', '品牌策略', '社交媒体', '广告创意',
            '用户体验', '数据分析', '内容营销', 'SEO优化', '品牌建设'
        ]
        
        tags = {}
        for tag_name in tags_data:
            tag_slug = slugify(tag_name)
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': tag_slug}
            )
            tags[tag_name] = tag
            if created:
                self.stdout.write(f'创建标签: {tag_name}')
        
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
            },
            {
                'title': '品牌年轻化的策略探讨',
                'content': '''传统品牌如何实现年轻化？这是一个值得深入探讨的话题。

**策略方向：**
1. 产品创新
2. 营销方式更新
3. 渠道拓展
4. 文化融合

有成功案例可以分享吗？''',
                'author': user2,
                'tags': ['品牌策略', '品牌建设', '创意设计']
            },
            {
                'title': 'SEO优化在2024年的新变化',
                'content': '''搜索引擎算法在不断更新，SEO策略也需要相应调整。

**新变化：**
- 用户体验权重提升
- 移动端优化重要性
- 内容质量要求更高
- 技术SEO新要求

大家有什么新的SEO策略可以分享？''',
                'author': user1,
                'tags': ['SEO优化', '数字营销', '数据分析']
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
                # 添加标签
                for tag_name in discussion_data['tags']:
                    discussion.tags.add(tags[tag_name])
                
                self.stdout.write(f'创建讨论: {discussion.title}')
                
                # 为每个讨论添加一些评论
                comments_data = [
                    {
                        'content': '非常详细的趋势分析，AI营销确实是未来的重点！',
                        'author': user2
                    },
                    {
                        'content': '同意楼主的观点，短视频营销现在确实很火。',
                        'author': user1
                    },
                    {
                        'content': '数据隐私保护这个点很重要，合规性不能忽视。',
                        'author': user2
                    }
                ]
                
                for j, comment_data in enumerate(comments_data):
                    comment = Comment.objects.create(
                        discussion=discussion,
                        content=comment_data['content'],
                        author=comment_data['author'],
                        created_at=discussion.created_at + timedelta(hours=j+1)
                    )
                    self.stdout.write(f'  添加评论: {comment.content[:30]}...')
                
                # 添加一些点赞
                if i % 2 == 0:
                    Like.objects.create(discussion=discussion, user=user2)
                if i % 3 == 0:
                    Like.objects.create(discussion=discussion, user=user1)
        
        self.stdout.write(self.style.SUCCESS('社区数据初始化完成！'))
        self.stdout.write(f'创建了 {Discussion.objects.count()} 个讨论')
        self.stdout.write(f'创建了 {Comment.objects.count()} 条评论')
        self.stdout.write(f'创建了 {Like.objects.count()} 个点赞')
        self.stdout.write(f'创建了 {Tag.objects.count()} 个标签') 