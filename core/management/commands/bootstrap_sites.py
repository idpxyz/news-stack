from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from core.models import HomePage

# 创建多站点
class Command(BaseCommand):
    help="Create example multi-sites (port=9000) and their HomePage roots"
    def ensure_site(self, hostname, site_name, port=9000, is_default=False):
        root=Page.get_first_root_node()
        if Site.objects.filter(hostname=hostname,port=port).exists():
            self.stdout.write(f"Site exists: {hostname}:{port}"); return
        home=HomePage(title=site_name); root.add_child(instance=home); home.save_revision().publish()
        Site.objects.create(hostname=hostname,port=port,site_name=site_name,root_page=home,is_default_site=is_default)
        self.stdout.write(self.style.SUCCESS(f"Created site: {hostname}:{port}"))
    def handle(self,*args,**opts):
        self.ensure_site("media1.local","Media One",port=9000,is_default=True)
        self.ensure_site("media2.local","Media Two",port=9000)
