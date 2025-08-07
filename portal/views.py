from django.http import JsonResponse
from django.conf import settings
from wagtail.models import Site
from news.models import ArticlePage, Channel

def _serialize_article(a):
    return {"id":a.id,"title":a.title,"date":a.date.isoformat() if a.date else None,
            "url":a.get_full_url() if hasattr(a,"get_full_url") else a.url,
            "site":a.get_site().hostname if hasattr(a,"get_site") else None,
            "channels":[c.slug for c in a.channels.all()],
            "has_image":bool(a.hero_image_id)}

def api_home(request):
    site=request.GET.get("site") or request.site.hostname
    s=Site.objects.filter(hostname=site).first() or request.site
    home=s.root_page.specific
    ctx=home.get_context(request)
    mods=[{"title":m.get("title"),"items":[_serialize_article(a) for a in m.get("items",[])]} for m in ctx.get("modules",[])]
    return JsonResponse({"site":s.hostname,"featured":[_serialize_article(a) for a in ctx.get("featured",[])],"modules":mods})

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
