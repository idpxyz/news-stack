from django.core.management.base import BaseCommand, CommandError
from wagtail.models import Page, Site
from core.models import HomePage
from django.utils import timezone

class Command(BaseCommand):
    help = "Create a new Wagtail site with homepage"
    
    def add_arguments(self, parser):
        parser.add_argument(
            'hostname',
            type=str,
            help='Site hostname (e.g., news.local)'
        )
        parser.add_argument(
            'site_name',
            type=str,
            help='Site display name (e.g., News Site)'
        )
        parser.add_argument(
            '--port',
            type=int,
            default=9000,
            help='Site port (default: 9000)'
        )
        parser.add_argument(
            '--default',
            action='store_true',
            help='Set as default site'
        )
        parser.add_argument(
            '--create-content',
            action='store_true',
            help='Create sample content for the site'
        )
    
    def handle(self, *args, **options):
        hostname = options['hostname']
        site_name = options['site_name']
        port = options['port']
        is_default = options['default']
        create_content = options['create_content']
        
        # 检查站点是否已存在
        if Site.objects.filter(hostname=hostname, port=port).exists():
            self.stdout.write(
                self.style.WARNING(f"Site already exists: {hostname}:{port}")
            )
            return
        
        try:
            # 获取根节点
            root = Page.get_first_root_node()
            
            # 创建首页
            home = HomePage(
                title=site_name,
                slug=hostname.replace('.', '-'),
                seo_title=f"{site_name} - 首页",
                search_description=f"{site_name} 的首页"
            )
            root.add_child(instance=home)
            home.save_revision().publish()
            
            # 创建站点
            site = Site.objects.create(
                hostname=hostname,
                port=port,
                site_name=site_name,
                root_page=home,
                is_default_site=is_default
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Created site: {hostname}:{port} ({site_name})"
                )
            )
            
            # 如果需要创建示例内容
            if create_content:
                self.create_sample_content(home, site_name)
            
            # 显示访问信息
            self.stdout.write(
                self.style.SUCCESS(
                    f"🌐 Access your site at: http://{hostname}:{port}/"
                )
            )
            
            # 提醒配置hosts文件
            self.stdout.write(
                self.style.WARNING(
                    f"💡 Don't forget to add to your hosts file:\n"
                    f"   127.0.0.1 {hostname}"
                )
            )
            
        except Exception as e:
            raise CommandError(f"Failed to create site: {str(e)}")
    
    def create_sample_content(self, home_page, site_name):
        """为站点创建示例内容"""
        from news.models import SectionIndexPage, ArticlePage, Channel
        from django.utils import timezone
        from datetime import timedelta
        import random
        
        # 创建分类页面
        section = SectionIndexPage(
            title=f"{site_name}新闻",
            slug="news",
            intro=f"欢迎访问{site_name}的新闻分类"
        )
        home_page.add_child(instance=section)
        section.save_revision().publish()
        
        # 获取频道
        channels = list(Channel.objects.all())
        
        # 创建示例文章
        for i in range(5):
            channel = random.choice(channels) if channels else None
            
            article = ArticlePage(
                title=f"{site_name}示例文章 {i+1}",
                slug=f"article-{i+1}",
                date=timezone.now() - timedelta(hours=i*2),
                is_featured=(i == 0),  # 第一篇文章设为特色
                feature_rank=random.randint(0, 10)
            )
            section.add_child(instance=article)
            article.save_revision().publish()
            
            # 添加频道标签
            if channel:
                article.channels.add(channel)
        
        self.stdout.write(
            self.style.SUCCESS(f"📝 Created sample content for {site_name}")
        ) 