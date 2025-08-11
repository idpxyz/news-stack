from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from wagtail.images.models import Image
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

class Discussion(models.Model):
    """讨论话题"""
    title = models.CharField(max_length=200, verbose_name="话题标题")
    content = models.TextField(verbose_name="话题内容")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussions')
    
    # 分类
    DISCUSSION_CATEGORIES = [
        ('general', '一般讨论'),
        ('industry', '行业话题'),
        ('creative', '创意分享'),
        ('technology', '技术交流'),
        ('career', '职业发展'),
        ('events', '活动讨论'),
    ]
    
    category = models.CharField(
        max_length=20,
        choices=DISCUSSION_CATEGORIES,
        default='general',
        verbose_name="讨论分类"
    )
    
    # 标签 - 使用CharField简化
    tags = models.CharField(max_length=200, blank=True, verbose_name="标签")
    
    # 统计
    views_count = models.IntegerField(default=0, verbose_name="浏览次数")
    replies_count = models.IntegerField(default=0, verbose_name="回复数量")
    likes_count = models.IntegerField(default=0, verbose_name="点赞数量")
    
    # 状态
    is_pinned = models.BooleanField(default=False, verbose_name="置顶")
    is_closed = models.BooleanField(default=False, verbose_name="已关闭")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    panels = [
        FieldPanel('title'),
        FieldPanel('content'),
        FieldPanel('category'),
        FieldPanel('tags'),
        MultiFieldPanel([
            FieldPanel('is_pinned'),
            FieldPanel('is_closed'),
        ], heading="状态设置"),
    ]
    
    class Meta:
        verbose_name = "讨论话题"
        verbose_name_plural = "讨论话题"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    """评论系统"""
    content = models.TextField(verbose_name="评论内容")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='comments')
    
    # 回复功能
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    
    # 统计
    likes_count = models.IntegerField(default=0, verbose_name="点赞数量")
    
    # 状态
    is_approved = models.BooleanField(default=True, verbose_name="已审核")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论"
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.author.username} 的评论"

class Like(models.Model):
    """点赞系统"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='likes')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'discussion')
        verbose_name = "点赞"
        verbose_name_plural = "点赞"
    
    def __str__(self):
        return f"{self.user.username} 点赞了 {self.discussion.title}"

class Notification(models.Model):
    """通知系统"""
    NOTIFICATION_TYPES = [
        ('comment', '新评论'),
        ('like', '新点赞'),
        ('follow', '新关注'),
        ('mention', '被提及'),
        ('reply', '回复'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications', null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    
    # 通用外键，关联到相关对象
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    message = models.CharField(max_length=200, verbose_name="通知消息")
    is_read = models.BooleanField(default=False, verbose_name="已读")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "通知"
        verbose_name_plural = "通知"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.recipient.username} - {self.get_notification_type_display()}"

class Tag(models.Model):
    """标签系统"""
    name = models.CharField(max_length=50, unique=True, verbose_name="标签名")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="标签别名")
    description = models.TextField(blank=True, verbose_name="标签描述")
    usage_count = models.IntegerField(default=0, verbose_name="使用次数")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"
        ordering = ['-usage_count']
    
    def __str__(self):
        return self.name

class Bookmark(models.Model):
    """书签系统"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    
    # 通用外键，可以收藏任何内容
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
        verbose_name = "书签"
        verbose_name_plural = "书签"
    
    def __str__(self):
        return f"{self.user.username} 收藏了 {self.content_object}" 