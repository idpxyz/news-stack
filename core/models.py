from django.db import models
from wagtail.models import Page, Orderable, Site
from wagtail.fields import StreamField
from wagtail.blocks import StructBlock, IntegerBlock, BooleanBlock, ChoiceBlock, CharBlock, TextBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel, MultiFieldPanel
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
    
    panels = [
        MultiFieldPanel([
            FieldPanel("default_limit"),
            FieldPanel("only_with_image_default"),
            FieldPanel("hot_time_window_hours"),
            FieldPanel("featured_target"),
            FieldPanel("module_backfill_cross_channel"),
        ], heading="首页内容配置"),
    ]
    
    class Meta:
        verbose_name = "首页设置"
        verbose_name_plural = "首页设置"

@register_setting
class SiteTheme(BaseSiteSetting):
    """站点UI主题设置"""
    THEME_CHOICES = [
        ("default", "默认主题"),
        ("dark", "深色主题"),
        ("light", "浅色主题"),
        ("news", "新闻主题"),
        ("tech", "科技主题"),
    ]
    
    theme = models.CharField(
        max_length=20, 
        choices=THEME_CHOICES, 
        default="default",
        verbose_name="主题样式"
    )
    
    primary_color = models.CharField(
        max_length=7, 
        default="#007bff",
        verbose_name="主色调",
        help_text="十六进制颜色值，如 #007bff"
    )
    
    logo_url = models.URLField(
        blank=True,
        verbose_name="Logo地址",
        help_text="站点Logo的URL地址"
    )
    
    favicon_url = models.URLField(
        blank=True,
        verbose_name="Favicon地址",
        help_text="浏览器标签页图标地址"
    )
    
    custom_css = models.TextField(
        blank=True,
        verbose_name="自定义CSS",
        help_text="额外的CSS样式代码"
    )
    
    panels = [
        MultiFieldPanel([
            FieldPanel("theme"),
            FieldPanel("primary_color"),
        ], heading="主题配置"),
        MultiFieldPanel([
            FieldPanel("logo_url"),
            FieldPanel("favicon_url"),
        ], heading="品牌配置"),
        FieldPanel("custom_css"),
    ]
    
    class Meta:
        verbose_name = "站点主题"
        verbose_name_plural = "站点主题"

@register_setting
class SEOSettings(BaseSiteSetting):
    """SEO设置"""
    meta_title = models.CharField(
        max_length=60,
        blank=True,
        verbose_name="默认标题",
        help_text="站点默认的页面标题（60字符以内）"
    )
    
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        verbose_name="默认描述",
        help_text="站点默认的页面描述（160字符以内）"
    )
    
    meta_keywords = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="默认关键词",
        help_text="站点默认的关键词，用逗号分隔"
    )
    
    google_analytics_id = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Google Analytics ID",
        help_text="GA4的测量ID，如 G-XXXXXXXXXX"
    )
    
    baidu_tongji_id = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="百度统计ID",
        help_text="百度统计的代码ID"
    )
    
    robots_txt = models.TextField(
        blank=True,
        verbose_name="Robots.txt内容",
        help_text="自定义robots.txt内容"
    )
    
    panels = [
        MultiFieldPanel([
            FieldPanel("meta_title"),
            FieldPanel("meta_description"),
            FieldPanel("meta_keywords"),
        ], heading="基础SEO"),
        MultiFieldPanel([
            FieldPanel("google_analytics_id"),
            FieldPanel("baidu_tongji_id"),
        ], heading="统计代码"),
        FieldPanel("robots_txt"),
    ]
    
    class Meta:
        verbose_name = "SEO设置"
        verbose_name_plural = "SEO设置"

@register_setting
class AdSettings(BaseSiteSetting):
    """广告设置"""
    ad_enabled = models.BooleanField(
        default=False,
        verbose_name="启用广告",
        help_text="是否在站点显示广告"
    )
    
    header_ad_slot = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="头部广告位ID",
        help_text="页面头部广告位的ID"
    )
    
    sidebar_ad_slot = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="侧边栏广告位ID",
        help_text="侧边栏广告位的ID"
    )
    
    footer_ad_slot = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="底部广告位ID",
        help_text="页面底部广告位的ID"
    )
    
    article_ad_slot = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="文章内广告位ID",
        help_text="文章内容中广告位的ID"
    )
    
    ad_network = models.CharField(
        max_length=50,
        choices=[
            ("google", "Google AdSense"),
            ("baidu", "百度联盟"),
            ("tencent", "腾讯广告"),
            ("custom", "自定义"),
        ],
        default="google",
        verbose_name="广告网络"
    )
    
    ad_code = models.TextField(
        blank=True,
        verbose_name="广告代码",
        help_text="自定义广告代码（HTML/JavaScript）"
    )
    
    panels = [
        MultiFieldPanel([
            FieldPanel("ad_enabled"),
            FieldPanel("ad_network"),
        ], heading="广告开关"),
        MultiFieldPanel([
            FieldPanel("header_ad_slot"),
            FieldPanel("sidebar_ad_slot"),
            FieldPanel("footer_ad_slot"),
            FieldPanel("article_ad_slot"),
        ], heading="广告位配置"),
        FieldPanel("ad_code"),
    ]
    
    class Meta:
        verbose_name = "广告设置"
        verbose_name_plural = "广告设置"

@register_setting
class SocialSettings(BaseSiteSetting):
    """社交媒体设置"""
    wechat_qr = models.URLField(
        blank=True,
        verbose_name="微信二维码",
        help_text="微信公众号二维码图片地址"
    )
    
    weibo_url = models.URLField(
        blank=True,
        verbose_name="微博地址",
        help_text="官方微博主页地址"
    )
    
    douyin_url = models.URLField(
        blank=True,
        verbose_name="抖音地址",
        help_text="官方抖音主页地址"
    )
    
    bilibili_url = models.URLField(
        blank=True,
        verbose_name="B站地址",
        help_text="官方B站主页地址"
    )
    
    contact_email = models.EmailField(
        blank=True,
        verbose_name="联系邮箱",
        help_text="官方联系邮箱"
    )
    
    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="联系电话",
        help_text="官方联系电话"
    )
    
    panels = [
        MultiFieldPanel([
            FieldPanel("wechat_qr"),
            FieldPanel("weibo_url"),
            FieldPanel("douyin_url"),
            FieldPanel("bilibili_url"),
        ], heading="社交媒体"),
        MultiFieldPanel([
            FieldPanel("contact_email"),
            FieldPanel("contact_phone"),
        ], heading="联系方式"),
    ]
    
    class Meta:
        verbose_name = "社交媒体设置"
        verbose_name_plural = "社交媒体设置"

class HomePage(Page):
    modules=StreamField([("channel",ChannelModuleBlock())],use_json_field=True,blank=True)

    content_panels=Page.content_panels+[InlinePanel("featured_items",label="首页手动精选"),FieldPanel("modules")]
    parent_page_types=["wagtailcore.Page"]
    subpage_types=["news.SectionIndexPage"]

    def get_context(self,request):
        from news.models import ArticlePage, CreativeWorkPage, IndustryEventPage, ResearchReportPage
        from django.utils import timezone
        from datetime import timedelta
        ctx=super().get_context(request)
        
        # 获取站点
        site = Site.find_for_request(request) or Site.objects.filter(is_default_site=True).first()
        if not site:
            ctx["featured"] = []
            ctx["modules"] = []
            ctx["creative_works"] = []
            ctx["upcoming_events"] = []
            ctx["latest_reports"] = []
            ctx["latest_discussions"] = []
            return ctx
            
        site_root=site.root_page
        selected_ids=set()
        settings=HomeToggles.for_site(site)
        
        # 获取特色文章
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
        
        # 获取创意作品
        creative_works = CreativeWorkPage.objects.live().public().specific().descendant_of(site_root).order_by("-date")[:6]
        ctx["creative_works"] = creative_works
        
        # 获取即将举行的活动
        upcoming_events = IndustryEventPage.objects.live().public().specific().descendant_of(site_root).filter(
            event_date__gte=timezone.now()
        ).order_by("event_date")[:5]
        ctx["upcoming_events"] = upcoming_events
        
        # 获取最新研究报告
        latest_reports = ResearchReportPage.objects.live().public().specific().descendant_of(site_root).order_by("-publish_date")[:5]
        ctx["latest_reports"] = latest_reports
        
        # 暂时使用空列表，避免数据库表不存在的问题
        ctx["latest_discussions"] = []
        
        # 获取频道模块内容
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
