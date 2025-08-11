from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import requests
from wagtail.models import Page, Site
from news.models import ArticlePage, CreativeWorkPage, IndustryEventPage, ResearchReportPage, Channel
from community.models import Discussion

def _serialize_article(a):
    return {"id":a.id,"title":a.title,"date":a.date.isoformat() if a.date else None,
            "url":a.get_full_url() if hasattr(a,"get_full_url") else a.url,
            "site":a.get_site().hostname if hasattr(a,"get_site") else None,
            "channels":[c.slug for c in a.channels.all()],
            "has_image":bool(a.hero_image_id)}

def home_view(request):
    """简单的首页视图"""
    # 获取精选文章
    featured_articles = ArticlePage.objects.filter(is_featured=True).order_by('feature_rank')[:4]
    
    # 如果没有精选文章，获取最新的文章
    if not featured_articles.exists():
        featured_articles = ArticlePage.objects.order_by('-date')[:4]
    
    # 获取最新新闻
    latest_news = ArticlePage.objects.order_by('-date')[:8]
    
    # 获取频道
    channels = Channel.objects.filter(is_active=True).order_by('name')
    
    # 调试信息
    print(f"Found {featured_articles.count()} featured articles")
    print(f"Found {latest_news.count()} latest news")
    
    # 为文章添加自定义URL属性
    for article in featured_articles:
        try:
            print(f"Article: {article.title}, Slug: {article.slug}, ID: {article.id}")
            # 直接使用基于slug的URL，这是最可靠的方法
            article.custom_url = f"/article/{article.slug}/"
            print(f"Set custom_url: {article.custom_url}")
        except Exception as e:
            print(f"Error setting URL for article {article.id}: {e}")
            article.custom_url = "#"
    
    for article in latest_news:
        try:
            print(f"Article: {article.title}, Slug: {article.slug}, ID: {article.id}")
            # 直接使用基于slug的URL，这是最可靠的方法
            article.custom_url = f"/article/{article.slug}/"
            print(f"Set custom_url: {article.custom_url}")
        except Exception as e:
            print(f"Error setting URL for article {article.id}: {e}")
            article.custom_url = "#"
    
    context = {
        'featured': featured_articles,
        'modules': [{'title': '最新新闻', 'items': latest_news}],
        'channels': channels,
        'creative_works': [],
        'upcoming_events': [],
        'latest_reports': [],
        'latest_discussions': []
    }
    
    return render(request, 'core/home_page.html', context)

def api_home(request):
    try:
        site = request.GET.get("site") or getattr(request, 'site', None)
        if not site:
            # 如果没有site，获取默认站点
            site = Site.objects.filter(is_default_site=True).first()
        if not site:
            return JsonResponse({"error": "No site found"}, status=400)
            
        s = site
        home = s.root_page.specific
        ctx = home.get_context(request)
        mods = [{"title":m.get("title"),"items":[_serialize_article(a) for a in m.get("items",[])]} for m in ctx.get("modules",[])]
        return JsonResponse({"site":s.hostname,"featured":[_serialize_article(a) for a in ctx.get("featured",[])],"modules":mods})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def api_portal(request):
    limit=int(request.GET.get("limit",20))
    ch_slug=request.GET.get("channel")
    only_img=request.GET.get("only_image") in ("1","true","True")
    items=[]
    if settings.OS_ENABLED:
        import requests
        q={"size":limit,"sort":[{"date":{"order":"desc"}}],"query":{"bool":{"must":[]}}}
        if ch_slug: q["query"]["bool"]["must"].append({"term":{"channels.keyword": ch_slug}})
        if only_img: q["query"]["bool"]["must"].append({"term":{"has_image": True}})
        r=requests.post(f"{settings.OS_URL.rstrip('/')}/{settings.OS_INDEX}/_search",json=q,timeout=5)
        if r.status_code==200:
            hits=r.json().get("hits",{}).get("hits",[])
            for h in hits:
                s=h.get("_source",{})
                items.append({"id":s.get("id"),"title":s.get("title"),"date":s.get("date"),
                              "url":s.get("absolute_url"),"site":s.get("site_hostname"),
                              "channels":s.get("channels",[]),"has_image":s.get("has_image",False)})
    else:
        qs=ArticlePage.objects.live().public().specific().order_by("-date")
        if ch_slug:
            try:
                ch=Channel.objects.get(slug=ch_slug); qs=qs.filter(channels=ch)
            except Channel.DoesNotExist:
                qs=qs.none()
        if only_img: qs=qs.filter(hero_image__isnull=False)
        items=[_serialize_article(a) for a in qs.select_related("hero_image")[:limit]]
    return JsonResponse({"items":items})

def search_view(request):
    """搜索视图 - 类似今日头条的搜索功能"""
    query = request.GET.get('q', '').strip()
    results = []
    
    if query:
        # 搜索文章
        articles = ArticlePage.objects.live().public().search(query)[:10]
        for article in articles:
            results.append({
                'type': 'article',
                'title': article.title,
                'url': article.url,
                'excerpt': article.specific.body[:100] + '...' if article.specific.body else '',
                'date': article.date,
                'category': article.channels.first().name if article.channels.exists() else '新闻'
            })
        
        # 搜索创意作品
        works = CreativeWorkPage.objects.live().public().search(query)[:5]
        for work in works:
            results.append({
                'type': 'work',
                'title': work.title,
                'url': work.url,
                'excerpt': f'创意作品 - {work.agency}',
                'date': work.date,
                'category': '创意作品'
            })
        
        # 搜索行业活动
        events = IndustryEventPage.objects.live().public().search(query)[:5]
        for event in events:
            results.append({
                'type': 'event',
                'title': event.title,
                'url': event.url,
                'excerpt': f'行业活动 - {event.location}',
                'date': event.event_date,
                'category': '行业活动'
            })
        
        # 搜索研究报告
        reports = ResearchReportPage.objects.live().public().search(query)[:5]
        for report in reports:
            results.append({
                'type': 'report',
                'title': report.title,
                'url': report.url,
                'excerpt': f'研究报告 - {report.author}',
                'date': report.publish_date,
                'category': '研究报告'
            })
        
        # 搜索社区讨论
        discussions = Discussion.objects.filter(title__icontains=query)[:5]
        for discussion in discussions:
            results.append({
                'type': 'discussion',
                'title': discussion.title,
                'url': f'/community/discussions/{discussion.id}/',
                'excerpt': discussion.content[:100] + '...' if discussion.content else '',
                'date': discussion.created_at,
                'category': '社区讨论'
            })
        
        # 按日期排序
        results.sort(key=lambda x: x['date'], reverse=True)
    
    # 热门搜索词
    hot_searches = [
        '数字营销', '创意设计', '品牌策略', '社交媒体', '广告创意',
        '内容营销', '用户体验', '数据分析', '人工智能', '短视频'
    ]
    
    context = {
        'query': query,
        'results': results,
        'hot_searches': hot_searches,
        'result_count': len(results)
    }
    
    return render(request, 'search_results.html', context)

def channels_view(request):
    """频道列表页面"""
    # 获取所有活跃的频道
    channels = Channel.objects.filter(is_active=True).order_by('name')
    
    # 为每个频道获取文章数量
    for channel in channels:
        channel.article_count = channel.articles.count()
        channel.creative_count = channel.creative_works.count()
        channel.event_count = channel.events.count()
        channel.report_count = channel.reports.count()
    
    context = {
        'channels': channels,
    }
    
    return render(request, 'portal/channels.html', context)

def article_detail(request, slug):
    """文章详情页视图"""
    try:
        # 根据slug获取文章
        article = ArticlePage.objects.get(slug=slug)
        
        # 获取相关文章
        related_articles = ArticlePage.objects.filter(
            channels__in=article.channels.all()
        ).exclude(id=article.id).order_by('-date')[:4]
        
        context = {
            'article': article,
            'related_articles': related_articles,
        }
        
        return render(request, 'news/article_detail.html', context)
        
    except ArticlePage.DoesNotExist:
        # 如果文章不存在，返回404
        from django.shortcuts import get_object_or_404
        return get_object_or_404(ArticlePage, slug=slug)
    except Exception as e:
        # 其他错误
        print(f"Error in article_detail view: {e}")
        from django.http import Http404
        raise Http404("文章不存在")
