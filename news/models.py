from django.db import models
from wagtail.models import Page
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.blocks import StreamBlock, CharBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase

@register_snippet
class Channel(models.Model):
    name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=50,unique=True)
    is_active=models.BooleanField(default=True)
    panels=[FieldPanel("name"),FieldPanel("slug"),FieldPanel("is_active")]
    def __str__(self): return self.name

class ArticleBody(StreamBlock):
    heading=CharBlock()
    image=ImageChooserBlock()
    paragraph=CharBlock()

class SectionIndexPage(Page):
    intro=models.TextField(blank=True)
    parent_page_types=["core.HomePage"]
    subpage_types=["news.ArticlePage","news.SectionIndexPage"]
    content_panels=Page.content_panels+[FieldPanel("intro")]

class ArticleTag(TaggedItemBase):
    content_object = ParentalKey(
        'ArticlePage',
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

class ChannelsIndexPage(RoutablePageMixin, Page):
    parent_page_types=["core.HomePage"]
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



