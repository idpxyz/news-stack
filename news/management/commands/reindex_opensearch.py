from django.core.management.base import BaseCommand
from django.conf import settings
from wagtail.models import Site
from news.models import ArticlePage
import requests

class Command(BaseCommand):
    help="Reindex ArticlePage into OpenSearch (optional). Controlled by OS_ENABLED env var."

    def handle(self,*args,**options):
        if not settings.OS_ENABLED:
            self.stdout.write(self.style.WARNING("OS_ENABLED=0 -> skipping")); return
        index=settings.OS_INDEX; base=settings.OS_URL.rstrip("/")
        try: requests.put(f"{base}/{index}")
        except Exception as e: self.stdout.write(self.style.WARNING(f"Create index error: {e}"))
        total=0
        for site in Site.objects.all():
            root=site.root_page
            qs=ArticlePage.objects.live().public().specific().descendant_of(root)
            for a in qs:
                doc={"id":a.id,"site_id":site.id,"site_hostname":site.hostname,"title":a.title,
                     "date":a.date.isoformat() if a.date else None,"channels":[c.slug for c in a.channels.all()],
                     "has_image":bool(a.hero_image_id),"absolute_url":a.get_full_url()}
                try:
                    r=requests.post(f"{base}/{index}/_doc/{a.id}",json=doc)
                    if r.status_code not in (200,201): self.stdout.write(self.style.WARNING(f"Index error {a.id}: {r.text[:120]}"))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Index exception {a.id}: {e}"))
                total+=1
        self.stdout.write(self.style.SUCCESS(f"Indexed {total} docs into {index}"))
