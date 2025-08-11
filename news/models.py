from django.db import models
from wagtail.models import Page
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.blocks import StreamBlock, CharBlock, TextBlock, ChoiceBlock, URLBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase
from wagtail.blocks import StructBlock, IntegerBlock, BooleanBlock

@register_snippet
class Channel(models.Model):
    name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=50,unique=True)
    is_active=models.BooleanField(default=True)
    
    # 新增字段
    category_type = models.CharField(
        max_length=20,
        choices=[
            ('news', '新闻'),
            ('creative', '创意'),
            ('industry', '行业'),
            ('research', '研究'),
            ('events', '活动'),
        ],
        default='news',
        verbose_name="分类类型"
    )
    
    description = models.TextField(blank=True, verbose_name="分类描述")
    icon = models.CharField(max_length=50, blank=True, verbose_name="图标类名")
    
    panels=[
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("is_active"),
        FieldPanel("category_type"),
        FieldPanel("description"),
        FieldPanel("icon"),
    ]
    
    def __str__(self): return self.name

class ArticleBody(StreamBlock):
    heading=CharBlock()
    image=ImageChooserBlock()
    paragraph=CharBlock()

class SectionIndexPage(Page):
    intro=models.TextField(blank=True)
    parent_page_types=["core.HomePage"]
    subpage_types=["news.ArticlePage","news.SectionIndexPage","news.CreativeWorkPage","news.IndustryEventPage","news.ResearchReportPage"]
    content_panels=Page.content_panels+[FieldPanel("intro")]

class ArticleTag(TaggedItemBase):
    content_object = ParentalKey(
        'ArticlePage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class CreativeWorkTag(TaggedItemBase):
    content_object = ParentalKey(
        'CreativeWorkPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class EventTag(TaggedItemBase):
    content_object = ParentalKey(
        'IndustryEventPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class ReportTag(TaggedItemBase):
    content_object = ParentalKey(
        'ResearchReportPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class ArticlePage(Page):
    date=models.DateTimeField(db_index=True)
    hero_image=models.ForeignKey("wagtailimages.Image",null=True,blank=True,on_delete=models.SET_NULL,related_name="+")
    body=StreamField(ArticleBody(),use_json_field=True,blank=True)
    channels=ParentalManyToManyField("news.Channel",blank=True,related_name="articles")
    tags=ClusterTaggableManager(through="news.ArticleTag",blank=True)
    is_featured=models.BooleanField(default=False,db_index=True)
    feature_rank=models.IntegerField(default=0,db_index=True)
    parent_page_types=["news.SectionIndexPage"]
    subpage_types=[]
    content_panels=Page.content_panels+[FieldPanel("date"),FieldPanel("hero_image"),FieldPanel("body"),
        FieldPanel("channels"),FieldPanel("tags"),
        MultiFieldPanel([FieldPanel("is_featured"),FieldPanel("feature_rank")],heading="Promotion")]

# 创意作品页面
class CreativeWorkPage(Page):
    """创意作品页面 - 类似The Drum的Creative Works"""
    date = models.DateTimeField(db_index=True, verbose_name="发布日期")
    hero_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    
    # 创意作品特有字段
    agency = models.CharField(max_length=200, verbose_name="代理公司")
    client = models.CharField(max_length=200, verbose_name="客户")
    campaign_name = models.CharField(max_length=200, blank=True, verbose_name="活动名称")
    
    CREATIVE_CATEGORIES = [
        ('advertising', '广告'),
        ('design', '设计'),
        ('digital', '数字营销'),
        ('branding', '品牌'),
        ('social', '社交媒体'),
        ('video', '视频'),
        ('print', '平面'),
        ('outdoor', '户外'),
    ]
    
    category = models.CharField(
        max_length=20,
        choices=CREATIVE_CATEGORIES,
        default='advertising',
        verbose_name="创意类别"
    )
    
    awards = models.TextField(blank=True, verbose_name="获奖情况")
    video_url = models.URLField(blank=True, verbose_name="视频链接")
    project_url = models.URLField(blank=True, verbose_name="项目链接")
    
    # 作品描述
    brief = models.TextField(blank=True, verbose_name="项目简介")
    solution = models.TextField(blank=True, verbose_name="解决方案")
    results = models.TextField(blank=True, verbose_name="项目成果")
    
    # 标签和分类
    channels = ParentalManyToManyField("news.Channel", blank=True, related_name="creative_works")
    tags = ClusterTaggableManager(through="news.CreativeWorkTag", blank=True)
    is_featured = models.BooleanField(default=False, db_index=True, verbose_name="精选作品")
    feature_rank = models.IntegerField(default=0, db_index=True, verbose_name="精选排序")
    
    parent_page_types = ["news.SectionIndexPage"]
    subpage_types = []
    
    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("hero_image"),
        MultiFieldPanel([
            FieldPanel("agency"),
            FieldPanel("client"),
            FieldPanel("campaign_name"),
            FieldPanel("category"),
        ], heading="项目信息"),
        MultiFieldPanel([
            FieldPanel("brief"),
            FieldPanel("solution"),
            FieldPanel("results"),
        ], heading="项目详情"),
        MultiFieldPanel([
            FieldPanel("awards"),
            FieldPanel("video_url"),
            FieldPanel("project_url"),
        ], heading="相关链接"),
        FieldPanel("channels"),
        FieldPanel("tags"),
        MultiFieldPanel([
            FieldPanel("is_featured"),
            FieldPanel("feature_rank")
        ], heading="推广设置"),
    ]

# 行业活动页面
class IndustryEventPage(Page):
    """行业活动页面 - 类似The Drum的Events"""
    event_date = models.DateTimeField(verbose_name="活动日期")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="结束日期")
    location = models.CharField(max_length=200, verbose_name="活动地点")
    organizer = models.CharField(max_length=200, verbose_name="主办方")
    
    EVENT_TYPES = [
        ('conference', '会议'),
        ('awards', '颁奖典礼'),
        ('workshop', '工作坊'),
        ('exhibition', '展览'),
        ('networking', '社交活动'),
        ('webinar', '网络研讨会'),
    ]
    
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        default='conference',
        verbose_name="活动类型"
    )
    
    registration_url = models.URLField(blank=True, verbose_name="报名链接")
    ticket_price = models.CharField(max_length=100, blank=True, verbose_name="票价信息")
    
    # 活动详情
    description = models.TextField(verbose_name="活动描述")
    agenda = models.TextField(blank=True, verbose_name="活动议程")
    speakers = models.TextField(blank=True, verbose_name="演讲嘉宾")
    
    # 媒体
    hero_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    channels = ParentalManyToManyField("news.Channel", blank=True, related_name="events")
    tags = ClusterTaggableManager(through="news.EventTag", blank=True)
    
    parent_page_types = ["news.SectionIndexPage"]
    subpage_types = []
    
    content_panels = Page.content_panels + [
        FieldPanel("hero_image"),
        MultiFieldPanel([
            FieldPanel("event_date"),
            FieldPanel("end_date"),
            FieldPanel("location"),
            FieldPanel("organizer"),
            FieldPanel("event_type"),
        ], heading="活动基本信息"),
        MultiFieldPanel([
            FieldPanel("registration_url"),
            FieldPanel("ticket_price"),
        ], heading="报名信息"),
        MultiFieldPanel([
            FieldPanel("description"),
            FieldPanel("agenda"),
            FieldPanel("speakers"),
        ], heading="活动详情"),
        FieldPanel("channels"),
        FieldPanel("tags"),
    ]

# 研究报告页面
class ResearchReportPage(Page):
    """研究报告页面 - 类似The Drum的Research"""
    publish_date = models.DateTimeField(db_index=True, verbose_name="发布日期")
    hero_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    
    REPORT_TYPES = [
        ('industry', '行业报告'),
        ('consumer', '消费者洞察'),
        ('trend', '趋势分析'),
        ('case_study', '案例研究'),
        ('whitepaper', '白皮书'),
        ('survey', '调研报告'),
    ]
    
    report_type = models.CharField(
        max_length=20,
        choices=REPORT_TYPES,
        default='industry',
        verbose_name="报告类型"
    )
    
    author = models.CharField(max_length=200, verbose_name="作者/机构")
    download_url = models.URLField(blank=True, verbose_name="下载链接")
    is_free = models.BooleanField(default=True, verbose_name="免费下载")
    
    # 报告内容
    summary = models.TextField(verbose_name="报告摘要")
    key_findings = models.TextField(blank=True, verbose_name="关键发现")
    methodology = models.TextField(blank=True, verbose_name="研究方法")
    
    # 标签和分类
    channels = ParentalManyToManyField("news.Channel", blank=True, related_name="reports")
    tags = ClusterTaggableManager(through="news.ReportTag", blank=True)
    is_featured = models.BooleanField(default=False, db_index=True, verbose_name="精选报告")
    
    parent_page_types = ["news.SectionIndexPage"]
    subpage_types = []
    
    content_panels = Page.content_panels + [
        FieldPanel("publish_date"),
        FieldPanel("hero_image"),
        MultiFieldPanel([
            FieldPanel("report_type"),
            FieldPanel("author"),
            FieldPanel("download_url"),
            FieldPanel("is_free"),
        ], heading="报告信息"),
        MultiFieldPanel([
            FieldPanel("summary"),
            FieldPanel("key_findings"),
            FieldPanel("methodology"),
        ], heading="报告内容"),
        FieldPanel("channels"),
        FieldPanel("tags"),
        FieldPanel("is_featured"),
    ]

class ChannelsIndexPage(RoutablePageMixin, Page):
    parent_page_types=["core.HomePage", "wagtailcore.Page"]
    subpage_types=[]
    @route(r'^$')
    def index(self, request):
        from django.shortcuts import render
        channels=Channel.objects.filter(is_active=True).order_by("name")
        return render(request,"news/channels_index.html",{"page":self,"channels":channels})
    
    @route(r'^(?P<slug>[-\\w]+)/$')
    def by_channel(self, request, slug):
        from django.core.paginator import Paginator
        from django.shortcuts import render, get_object_or_404
        site_root=request.site.root_page
        ch=get_object_or_404(Channel,slug=slug,is_active=True)
        qs=ArticlePage.objects.live().public().specific().descendant_of(site_root).filter(channels=ch).order_by("-date")
        paginator=Paginator(qs,10)
        page_num=int(request.GET.get("page",1))
        page_obj=paginator.get_page(page_num)
        return render(request,"news/channel_landing.html",{"page":self,"channel":ch,"page_obj":page_obj,"items":page_obj.object_list})
