from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q, Count, F
from django.utils import timezone
import markdown
from .models import Discussion, Comment, Like, Tag
from django.contrib.auth.models import User

def markdown_to_html(text):
    """将Markdown文本转换为HTML"""
    if not text:
        return ''
    
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
            'markdown.extensions.nl2br',
        ]
    )
    return md.convert(str(text))

def markdown_to_preview(text, max_length=200):
    """将Markdown文本转换为适合预览的HTML，只保留基本格式"""
    if not text:
        return ''
    
    # 截取文本
    if len(text) > max_length:
        preview_text = text[:max_length] + '...'
    else:
        preview_text = text
    
    # 只使用基本的Markdown扩展，适合预览
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.nl2br',  # 换行转<br>
        ]
    )
    return md.convert(str(preview_text))

def discussion_list(request):
    """讨论列表页面"""
    discussions = Discussion.objects.select_related('author').annotate(
        comment_count=Count('comments'),
        like_count=Count('likes')
    ).order_by('-created_at')
    
    # 搜索功能
    query = request.GET.get('q')
    if query:
        discussions = discussions.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(tags__icontains=query)
        ).distinct()
    
    # 标签筛选
    tag_name = request.GET.get('tag')
    if tag_name:
        discussions = discussions.filter(tags__icontains=tag_name)
    
    # 分页
    paginator = Paginator(discussions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 为列表中的讨论内容添加Markdown处理
    for discussion in page_obj.object_list:
        # 为预览内容添加HTML版本
        discussion.content_preview = markdown_to_preview(discussion.content, 200)
    
    # 获取热门标签
    popular_tags = Tag.objects.all()[:10]
    
    context = {
        'page_obj': page_obj,
        'discussions': page_obj.object_list,
        'popular_tags': popular_tags,
        'query': query,
        'selected_tag': tag_name,
    }
    return render(request, 'community/discussion_list.html', context)

def discussion_detail(request, discussion_id):
    """讨论详情页面"""
    discussion = get_object_or_404(Discussion.objects.select_related('author'), id=discussion_id)
    
    # 获取评论
    comments = discussion.comments.select_related('author').order_by('created_at')
    
    # 检查用户是否已点赞
    user_liked = False
    if request.user.is_authenticated:
        user_liked = discussion.likes.filter(user=request.user).exists()
    
    # 处理Markdown内容
    discussion.content_html = markdown_to_html(discussion.content)
    
    # 处理评论的Markdown内容
    for comment in comments:
        comment.content_html = markdown_to_html(comment.content)
    
    context = {
        'discussion': discussion,
        'comments': comments,
        'user_liked': user_liked,
    }
    return render(request, 'community/discussion_detail.html', context)

@login_required
def create_discussion(request):
    """创建新讨论"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tag_names = request.POST.get('tags', '').split(',')
        
        if title and content:
            # 处理标签
            tags_str = ', '.join([tag.strip() for tag in tag_names if tag.strip()])
            
            discussion = Discussion.objects.create(
                title=title.strip(),
                content=content.strip(),
                author=request.user,
                tags=tags_str
            )
            
            messages.success(request, '讨论创建成功！')
            return redirect('community:discussion_detail', discussion_id=discussion.id)
        else:
            messages.error(request, '请填写标题和内容！')
    
    return render(request, 'community/create_discussion.html')

@login_required
@require_POST
def add_comment(request, discussion_id):
    """添加评论"""
    discussion = get_object_or_404(Discussion, id=discussion_id)
    content = request.POST.get('content')
    
    if content:
        comment = Comment.objects.create(
            discussion=discussion,
            author=request.user,
            content=content.strip()
        )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'comment': {
                    'id': comment.id,
                    'content': markdown_to_html(comment.content),
                    'author': comment.author.username,
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
                }
            })
        else:
            messages.success(request, '评论发表成功！')
    else:
        messages.error(request, '评论内容不能为空！')
    
    return redirect('community:discussion_detail', discussion_id=discussion_id)

@login_required
@require_POST
def toggle_like(request, discussion_id):
    """切换点赞状态"""
    discussion = get_object_or_404(Discussion, id=discussion_id)
    
    like, created = Like.objects.get_or_create(
        discussion=discussion,
        user=request.user
    )
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    return JsonResponse({
        'success': True,
        'liked': liked,
        'like_count': discussion.likes.count()
    })

def user_profile(request, username):
    """用户资料页面"""
    user = get_object_or_404(User, username=username)
    
    # 获取用户的讨论和评论
    discussions = Discussion.objects.filter(author=user).order_by('-created_at')[:10]
    comments = Comment.objects.filter(author=user).select_related('discussion').order_by('-created_at')[:10]
    
    context = {
        'profile_user': user,
        'discussions': discussions,
        'comments': comments,
    }
    return render(request, 'community/user_profile.html', context) 