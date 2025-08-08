from wagtail import hooks
from django.core.cache import caches
from django.core.cache.utils import make_template_fragment_key
from .models import HomeToggles

@hooks.register("after_publish_page") # 发布页面后清除首页缓存
def purge_home_cache_on_publish(request, page):
    cache=caches["default"]
    try:
        site=page.get_site()
    except Exception:
        site=None
    if not site:
        cache.clear(); return
    home=site.root_page.specific
    try:
        modules=getattr(home,"modules",[])
    except Exception:
        modules=[]
    settings=HomeToggles.for_site(site) #
    for block in modules:
        b=block.value
        title=b.get("title") or getattr(b.get("channel"),"name",None)
        if not title: continue
        ordering=b.get("ordering"); limit=b.get("limit"); only_img=b.get("only_with_image")
        ch=b.get("channel"); ch_slug=getattr(ch,"slug","na") if ch else "na"
        sig=f"ch:{ch_slug}|ord:{ordering}|lim:{limit}|img:{only_img}|xch:{settings.module_backfill_cross_channel}"
        key=make_template_fragment_key("home",[str(site.id),title,sig])
        cache.delete(key)
