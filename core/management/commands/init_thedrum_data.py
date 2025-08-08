from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from wagtail.models import Site
from news.models import Channel, ArticlePage, CreativeWorkPage, IndustryEventPage, ResearchReportPage
from core.models import HomePage

class Command(BaseCommand):
    help = "初始化The Drum风格的示例数据"

    def handle(self, *args, **options):
        self.stdout.write("🎯 开始初始化The Drum风格数据...")
        
        # 获取默认站点
        site = Site.objects.filter(is_default_site=True).first()
        if not site:
            self.stdout.write(self.style.ERROR("❌ 未找到默认站点"))
            return
        
        site_root = site.root_page
        
        # 创建频道分类
        self.create_channels()
        
        # 创建示例文章
        self.create_sample_articles(site_root)
        
        # 创建创意作品
        self.create_creative_works(site_root)
        
        # 创建行业活动
        self.create_industry_events(site_root)
        
        # 创建研究报告
        self.create_research_reports(site_root)
        
        self.stdout.write(self.style.SUCCESS("✅ The Drum风格数据初始化完成！"))

    def create_channels(self):
        """创建频道分类"""
        channels_data = [
            # 新闻分类
            {'name': '品牌', 'slug': 'brand', 'category_type': 'news', 'description': '品牌营销相关新闻'},
            {'name': '代理', 'slug': 'agency', 'category_type': 'news', 'description': '广告代理公司新闻'},
            {'name': '创意', 'slug': 'creative', 'category_type': 'creative', 'description': '创意设计作品'},
            {'name': '数字', 'slug': 'digital', 'category_type': 'news', 'description': '数字营销新闻'},
            {'name': '媒体', 'slug': 'media', 'category_type': 'news', 'description': '媒体行业新闻'},
            {'name': '技术', 'slug': 'tech', 'category_type': 'news', 'description': '技术趋势新闻'},
            {'name': '活动', 'slug': 'events', 'category_type': 'events', 'description': '行业活动信息'},
            {'name': '研究', 'slug': 'research', 'category_type': 'research', 'description': '行业研究报告'},
        ]
        
        for data in channels_data:
            channel, created = Channel.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            if created:
                self.stdout.write(f"  ✅ 创建频道: {channel.name}")
            else:
                self.stdout.write(f"  ℹ️  频道已存在: {channel.name}")

    def create_sample_articles(self, site_root):
        """创建示例文章"""
        articles_data = [
            {
                'title': '数字营销的未来：AI驱动的个性化体验',
                'channels': ['digital', 'tech'],
                'is_featured': True,
                'feature_rank': 1,
            },
            {
                'title': '品牌如何在小红书上建立影响力',
                'channels': ['brand', 'digital'],
                'is_featured': True,
                'feature_rank': 2,
            },
            {
                'title': '2024年广告创意趋势报告',
                'channels': ['creative', 'research'],
                'is_featured': True,
                'feature_rank': 3,
            },
            {
                'title': '独立广告代理公司的生存之道',
                'channels': ['agency'],
                'is_featured': False,
            },
            {
                'title': '短视频营销的黄金法则',
                'channels': ['digital', 'media'],
                'is_featured': False,
            },
            {
                'title': '元宇宙营销：品牌的新战场',
                'channels': ['tech', 'brand'],
                'is_featured': False,
            },
        ]
        
        for data in articles_data:
            article = ArticlePage(
                title=data['title'],
                date=timezone.now() - timedelta(days=len(articles_data) - articles_data.index(data)),
                body=[{'type': 'paragraph', 'value': f'这是{data["title"]}的详细内容。'}],
            )
            site_root.add_child(instance=article)
            
            # 添加频道
            for slug in data['channels']:
                try:
                    channel = Channel.objects.get(slug=slug)
                    article.channels.add(channel)
                except Channel.DoesNotExist:
                    pass
            
            # 设置特色状态
            if data.get('is_featured'):
                article.is_featured = True
                article.feature_rank = data['feature_rank']
                article.save()
            
            self.stdout.write(f"  ✅ 创建文章: {article.title}")

    def create_creative_works(self, site_root):
        """创建创意作品"""
        works_data = [
            {
                'title': 'Nike 2024春季广告系列',
                'agency': 'Wieden+Kennedy',
                'client': 'Nike',
                'category': 'advertising',
                'brief': '展现运动精神与时尚的完美结合',
            },
            {
                'title': 'Apple Vision Pro 品牌视觉设计',
                'agency': 'TBWA\Media Arts Lab',
                'client': 'Apple',
                'category': 'branding',
                'brief': '为苹果最新AR设备打造品牌视觉',
            },
            {
                'title': '可口可乐可持续包装设计',
                'agency': 'Turner Duckworth',
                'client': 'Coca-Cola',
                'category': 'design',
                'brief': '环保理念下的包装重新设计',
            },
            {
                'title': '小米汽车数字营销campaign',
                'agency': '华扬联众',
                'client': '小米',
                'category': 'digital',
                'brief': '小米首款汽车的线上营销推广',
            },
        ]
        
        for data in works_data:
            work = CreativeWorkPage(
                title=data['title'],
                date=timezone.now() - timedelta(days=works_data.index(data) * 2),
                agency=data['agency'],
                client=data['client'],
                category=data['category'],
                brief=data['brief'],
                solution=f'为{data["client"]}提供了创新的{data["category"]}解决方案',
                results='项目获得广泛好评，提升了品牌影响力',
            )
            site_root.add_child(instance=work)
            
            # 添加创意频道
            try:
                creative_channel = Channel.objects.get(slug='creative')
                work.channels.add(creative_channel)
            except Channel.DoesNotExist:
                pass
            
            self.stdout.write(f"  ✅ 创建创意作品: {work.title}")

    def create_industry_events(self, site_root):
        """创建行业活动"""
        events_data = [
            {
                'title': '2024中国广告节',
                'event_date': timezone.now() + timedelta(days=30),
                'location': '北京国家会议中心',
                'organizer': '中国广告协会',
                'event_type': 'conference',
                'description': '年度最大的广告行业盛会',
            },
            {
                'title': '戛纳创意节中国区选拔赛',
                'event_date': timezone.now() + timedelta(days=45),
                'location': '上海展览中心',
                'organizer': '戛纳创意节组委会',
                'event_type': 'awards',
                'description': '选拔优秀创意作品参加戛纳创意节',
            },
            {
                'title': '数字营销实战工作坊',
                'event_date': timezone.now() + timedelta(days=15),
                'location': '深圳腾讯大厦',
                'organizer': '腾讯广告学院',
                'event_type': 'workshop',
                'description': '深度解析数字营销策略与执行',
            },
        ]
        
        for data in events_data:
            event = IndustryEventPage(
                title=data['title'],
                event_date=data['event_date'],
                location=data['location'],
                organizer=data['organizer'],
                event_type=data['event_type'],
                description=data['description'],
                agenda='详细议程将在活动前一周公布',
                speakers='邀请行业专家和知名品牌代表',
            )
            site_root.add_child(instance=event)
            
            # 添加活动频道
            try:
                events_channel = Channel.objects.get(slug='events')
                event.channels.add(events_channel)
            except Channel.DoesNotExist:
                pass
            
            self.stdout.write(f"  ✅ 创建活动: {event.title}")

    def create_research_reports(self, site_root):
        """创建研究报告"""
        reports_data = [
            {
                'title': '2024年中国数字营销趋势报告',
                'report_type': 'trend',
                'author': '艾瑞咨询',
                'is_free': True,
                'summary': '深度分析2024年数字营销行业发展趋势',
            },
            {
                'title': 'Z世代消费者行为洞察',
                'report_type': 'consumer',
                'author': '尼尔森',
                'is_free': False,
                'summary': '揭示Z世代消费者的购买决策过程',
            },
            {
                'title': '短视频营销效果评估白皮书',
                'report_type': 'whitepaper',
                'author': '抖音营销研究院',
                'is_free': True,
                'summary': '短视频营销ROI分析与最佳实践',
            },
        ]
        
        for data in reports_data:
            report = ResearchReportPage(
                title=data['title'],
                publish_date=timezone.now() - timedelta(days=reports_data.index(data) * 7),
                report_type=data['report_type'],
                author=data['author'],
                is_free=data['is_free'],
                summary=data['summary'],
                key_findings='报告揭示了重要的市场洞察和趋势',
                methodology='采用定量与定性相结合的研究方法',
            )
            site_root.add_child(instance=report)
            
            # 添加研究频道
            try:
                research_channel = Channel.objects.get(slug='research')
                report.channels.add(research_channel)
            except Channel.DoesNotExist:
                pass
            
            self.stdout.write(f"  ✅ 创建报告: {report.title}") 