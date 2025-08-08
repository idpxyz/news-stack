from django.core.management.base import BaseCommand
from wagtail.models import Site
from core.models import SiteTheme, SEOSettings, AdSettings, SocialSettings

class Command(BaseCommand):
    help = "为所有站点初始化默认设置"

    def handle(self, *args, **options):
        sites = Site.objects.all()
        
        for site in sites:
            self.stdout.write(f"处理站点: {site.site_name} ({site.hostname}:{site.port})")
            
            # 初始化主题设置
            theme, created = SiteTheme.objects.get_or_create(site=site)
            if created:
                self.stdout.write(f"  ✅ 创建主题设置")
            else:
                self.stdout.write(f"  ℹ️  主题设置已存在")
            
            # 初始化SEO设置
            seo, created = SEOSettings.objects.get_or_create(site=site)
            if created:
                self.stdout.write(f"  ✅ 创建SEO设置")
            else:
                self.stdout.write(f"  ℹ️  SEO设置已存在")
            
            # 初始化广告设置
            ad, created = AdSettings.objects.get_or_create(site=site)
            if created:
                self.stdout.write(f"  ✅ 创建广告设置")
            else:
                self.stdout.write(f"  ℹ️  广告设置已存在")
            
            # 初始化社交媒体设置
            social, created = SocialSettings.objects.get_or_create(site=site)
            if created:
                self.stdout.write(f"  ✅ 创建社交媒体设置")
            else:
                self.stdout.write(f"  ℹ️  社交媒体设置已存在")
        
        self.stdout.write(self.style.SUCCESS(f"\n✅ 完成！已为 {sites.count()} 个站点初始化设置"))
        self.stdout.write("\n📝 接下来您可以：")
        self.stdout.write("  1. 访问 /admin/settings/ 配置站点设置")
        self.stdout.write("  2. 在管理后台的 Settings 菜单中查看所有设置")
        self.stdout.write("  3. 每个站点可以独立配置主题、SEO、广告等") 