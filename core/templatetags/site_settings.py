from django import template
from wagtail.models import Site
from core.models import SiteTheme, SEOSettings, AdSettings, SocialSettings

register = template.Library()

@register.simple_tag(takes_context=True)
def get_site_theme(context):
    """获取站点主题设置"""
    request = context.get('request')
    if not request:
        return None
    
    site = Site.find_for_request(request) or Site.objects.filter(is_default_site=True).first()
    if not site:
        return None
    
    try:
        return SiteTheme.for_site(site)
    except SiteTheme.DoesNotExist:
        return None

@register.simple_tag(takes_context=True)
def get_seo_settings(context):
    """获取SEO设置"""
    request = context.get('request')
    if not request:
        return None
    
    site = Site.find_for_request(request) or Site.objects.filter(is_default_site=True).first()
    if not site:
        return None
    
    try:
        return SEOSettings.for_site(site)
    except SEOSettings.DoesNotExist:
        return None

@register.simple_tag(takes_context=True)
def get_ad_settings(context):
    """获取广告设置"""
    request = context.get('request')
    if not request:
        return None
    
    site = Site.find_for_request(request) or Site.objects.filter(is_default_site=True).first()
    if not site:
        return None
    
    try:
        return AdSettings.for_site(site)
    except AdSettings.DoesNotExist:
        return None

@register.simple_tag(takes_context=True)
def get_social_settings(context):
    """获取社交媒体设置"""
    request = context.get('request')
    if not request:
        return None
    
    site = Site.find_for_request(request) or Site.objects.filter(is_default_site=True).first()
    if not site:
        return None
    
    try:
        return SocialSettings.for_site(site)
    except SocialSettings.DoesNotExist:
        return None

@register.simple_tag(takes_context=True)
def get_theme_css_class(context):
    """获取主题CSS类名"""
    theme = get_site_theme(context)
    if theme and theme.theme != 'default':
        return f'theme-{theme.theme}'
    return ''

@register.simple_tag(takes_context=True)
def get_primary_color(context):
    """获取主色调"""
    theme = get_site_theme(context)
    if theme:
        return theme.primary_color
    return '#007bff'

@register.simple_tag(takes_context=True)
def get_logo_url(context):
    """获取Logo地址"""
    theme = get_site_theme(context)
    if theme and theme.logo_url:
        return theme.logo_url
    return ''

@register.simple_tag(takes_context=True)
def get_favicon_url(context):
    """获取Favicon地址"""
    theme = get_site_theme(context)
    if theme and theme.favicon_url:
        return theme.favicon_url
    return ''

@register.simple_tag(takes_context=True)
def get_custom_css(context):
    """获取自定义CSS"""
    theme = get_site_theme(context)
    if theme and theme.custom_css:
        return theme.custom_css
    return ''

@register.simple_tag(takes_context=True)
def get_google_analytics_id(context):
    """获取Google Analytics ID"""
    seo = get_seo_settings(context)
    if seo and seo.google_analytics_id:
        return seo.google_analytics_id
    return ''

@register.simple_tag(takes_context=True)
def get_baidu_tongji_id(context):
    """获取百度统计ID"""
    seo = get_seo_settings(context)
    if seo and seo.baidu_tongji_id:
        return seo.baidu_tongji_id
    return ''

@register.simple_tag(takes_context=True)
def is_ad_enabled(context):
    """检查是否启用广告"""
    ad_settings = get_ad_settings(context)
    return ad_settings and ad_settings.ad_enabled

@register.simple_tag(takes_context=True)
def get_ad_slot(context, slot_name):
    """获取指定广告位ID"""
    ad_settings = get_ad_settings(context)
    if not ad_settings:
        return ''
    
    slot_map = {
        'header': ad_settings.header_ad_slot,
        'sidebar': ad_settings.sidebar_ad_slot,
        'footer': ad_settings.footer_ad_slot,
        'article': ad_settings.article_ad_slot,
    }
    
    return slot_map.get(slot_name, '')

@register.simple_tag(takes_context=True)
def get_ad_network(context):
    """获取广告网络"""
    ad_settings = get_ad_settings(context)
    if ad_settings:
        return ad_settings.ad_network
    return 'google'

@register.simple_tag(takes_context=True)
def get_ad_code(context):
    """获取自定义广告代码"""
    ad_settings = get_ad_settings(context)
    if ad_settings and ad_settings.ad_code:
        return ad_settings.ad_code
    return ''

@register.simple_tag(takes_context=True)
def get_wechat_qr(context):
    """获取微信二维码"""
    social = get_social_settings(context)
    if social and social.wechat_qr:
        return social.wechat_qr
    return ''

@register.simple_tag(takes_context=True)
def get_weibo_url(context):
    """获取微博地址"""
    social = get_social_settings(context)
    if social and social.weibo_url:
        return social.weibo_url
    return ''

@register.simple_tag(takes_context=True)
def get_contact_email(context):
    """获取联系邮箱"""
    social = get_social_settings(context)
    if social and social.contact_email:
        return social.contact_email
    return ''

@register.simple_tag(takes_context=True)
def get_contact_phone(context):
    """获取联系电话"""
    social = get_social_settings(context)
    if social and social.contact_phone:
        return social.contact_phone
    return '' 