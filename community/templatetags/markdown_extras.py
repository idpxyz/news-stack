from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter(name='markdown')
def markdown_filter(value):
    """
    将Markdown文本转换为HTML
    """
    if not value:
        return ''
    
    # 配置Markdown扩展
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.fenced_code',      # 代码块
            'markdown.extensions.codehilite',       # 代码高亮
            'markdown.extensions.tables',           # 表格
            'markdown.extensions.toc',              # 目录
            'markdown.extensions.footnotes',        # 脚注
            'markdown.extensions.def_list',         # 定义列表
            'markdown.extensions.abbr',             # 缩写
            'markdown.extensions.attr_list',        # 属性列表
            'markdown.extensions.nl2br',            # 换行转<br>
        ],
        extension_configs={
            'codehilite': {
                'css_class': 'highlight',
                'use_pygments': True,
                'noclasses': True,
            }
        }
    )
    
    # 转换Markdown为HTML
    html = md.convert(str(value))
    
    # 返回安全的HTML
    return mark_safe(html)

@register.filter(name='markdown_simple')
def markdown_simple_filter(value):
    """
    简单的Markdown渲染，只包含基本功能
    """
    if not value:
        return ''
    
    # 配置基本的Markdown扩展
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.fenced_code',      # 代码块
            'markdown.extensions.tables',           # 表格
            'markdown.extensions.nl2br',            # 换行转<br>
        ]
    )
    
    # 转换Markdown为HTML
    html = md.convert(str(value))
    
    # 返回安全的HTML
    return mark_safe(html) 