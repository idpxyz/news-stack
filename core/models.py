from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import StreamField
from wagtail.blocks import StructBlock, IntegerBlock, BooleanBlock, ChoiceBlock, CharBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from modelcluster.fields import ParentalKey

ORDER_CHOICES=[("-is_featured,-feature_rank,-date","置顶优先/最新"),("-date","最新")]

class ChannelModuleBlock(StructBlock):
    title=CharBlock(required=False)
    channel=SnippetChooserBlock(target_model="news.Channel",required=True)
    limit=IntegerBlock(default=8,min_value=1,max_value=50)
    only_with_image=BooleanBlock(required=False)
    ordering=ChoiceBlock(choices=ORDER_CHOICES,default="-is_featured,-feature_rank,-date")
    class Meta: icon="list-ul"; label="频道内容模块"

class FeaturedItem(Orderable):
    page=ParentalKey("core.HomePage",related_name="featured_items",on_delete=models.CASCADE)
    article=models.ForeignKey("news.ArticlePage",on_delete=models.CASCADE,related_name="+")
    note=models.CharField(max_length=120,blank=True)
    panels=[PageChooserPanel("article",["news.ArticlePage"])]

@register_setting
class HomeToggles(BaseSiteSetting):
    default_limit=models.IntegerField(default=8)
    only_with_image_default=models.BooleanField(default=False)
    hot_time_window_hours=models.IntegerField(default=72)
    featured_target=models.IntegerField(default=4,help_text="首页精选目标条数，不足时自动补齐")
    module_backfill_cross_channel=models.BooleanField(default=False,help_text="模块不足位是否允许跨频道补齐")

class HomePage(Page):
    modules=StreamField([("channel",ChannelModuleBlock())],use_json_field=True,blank=True)

    content_panels=Page.content_panels+[InlinePanel("featured_items",label="首页手动精选"),FieldPanel("modules")]
    parent_page_types=["wagtailcore.Page"]
    subpage_types=["news.SectionIndexPage"]

    def get_context(self,request):
        from news.models import ArticlePage
        from django.utils import timezone
        from datetime import timedelta
        ctx=super().get_context(request)
        site_root=request.site.root_page
        selected_ids=set()
        settings=HomeToggles.for_site(request.site)
        manual=[fi.article.specific for fi in self.featured_items.select_related("article")]
        manual=[a for a in manual if a.is_descendant_of(site_root)]
        selected_ids|={a.id for a in manual}
        target=max(0,settings.featured_target-len(manual))
        if target:
            qs=ArticlePage.objects.live().public().specific().descendant_of(site_root)
            if settings.only_with_image_default: qs=qs.filter(hero_image__isnull=False)
            if settings.hot_time_window_hours>0: qs=qs.filter(date__gte=timezone.now()-timedelta(hours=settings.hot_time_window_hours))
            qs=qs.exclude(id__in=selected_ids).order_by("-is_featured","-feature_rank","-date")[:target]
            backfill=list(qs); manual.extend(backfill); selected_ids|={a.id for a in backfill}
        ctx["featured"]=manual
        modules_out=[]
        for block in self.modules:
            b=block.value
            ch=b["channel"]
            qs=ArticlePage.objects.live().public().specific().descendant_of(site_root).filter(channels=ch)
            only_img=b.get("only_with_image",settings.only_with_image_default)
            if only_img: qs=qs.filter(hero_image__isnull=False)
            order_by=[o for o in b["ordering"].split(",") if o]
            limit=b.get("limit") or settings.default_limit
            qs=qs.exclude(id__in=selected_ids).order_by(*order_by).select_related("hero_image")[:limit]
            items=list(qs)
            need=limit-len(items)
            if need>0:
                backfill_qs=ArticlePage.objects.live().public().specific().descendant_of(site_root)
                if not settings.module_backfill_cross_channel: backfill_qs=backfill_qs.filter(channels=ch)
                if only_img: backfill_qs=backfill_qs.filter(hero_image__isnull=False)
                backfill_qs=backfill_qs.exclude(id__in=selected_ids|{p.id for p in items}).order_by(*order_by)[:need]
                items.extend(list(backfill_qs))
            selected_ids|={p.id for p in items}
            sig=f"ch:{getattr(ch,'slug','na')}|ord:{b.get('ordering')}|lim:{limit}|img:{only_img}|xch:{settings.module_backfill_cross_channel}"
            modules_out.append({"title": b.get("title") or ch.name,"items":items,"sig":sig,"channel_slug":getattr(ch,"slug",None)})
        ctx["modules"]=modules_out
        return ctx
