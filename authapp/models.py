from django.db import models
from django.contrib.auth.models import User
from wagtail.images.models import Image
from wagtail.admin.panels import MultiFieldPanel, FieldPanel

class UserProfile(models.Model):
    """用户资料扩展"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # 基本信息
    company = models.CharField(max_length=200, blank=True, verbose_name="公司")
    position = models.CharField(max_length=100, blank=True, verbose_name="职位")
    industry = models.CharField(max_length=100, blank=True, verbose_name="行业")
    bio = models.TextField(blank=True, verbose_name="个人简介")
    avatar = models.ForeignKey(
        Image, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='+',
        verbose_name="头像"
    )
    
    # 社交媒体
    website = models.URLField(blank=True, verbose_name="个人网站")
    twitter = models.CharField(max_length=100, blank=True, verbose_name="Twitter")
    linkedin = models.CharField(max_length=100, blank=True, verbose_name="LinkedIn")
    
    # 贡献者功能
    is_contributor = models.BooleanField(default=False, verbose_name="是否为贡献者")
    contributor_bio = models.TextField(blank=True, verbose_name="贡献者简介")
    contributor_expertise = models.CharField(max_length=200, blank=True, verbose_name="专业领域")
    
    # 统计信息
    articles_count = models.IntegerField(default=0, verbose_name="文章数量")
    followers_count = models.IntegerField(default=0, verbose_name="关注者数量")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    panels = [
        FieldPanel('avatar'),
        MultiFieldPanel([
            FieldPanel('company'),
            FieldPanel('position'),
            FieldPanel('industry'),
            FieldPanel('bio'),
        ], heading="基本信息"),
        MultiFieldPanel([
            FieldPanel('website'),
            FieldPanel('twitter'),
            FieldPanel('linkedin'),
        ], heading="社交媒体"),
        MultiFieldPanel([
            FieldPanel('is_contributor'),
            FieldPanel('contributor_bio'),
            FieldPanel('contributor_expertise'),
        ], heading="贡献者信息"),
    ]
    
    def __str__(self):
        return f"{self.user.username} 的资料"
    
    class Meta:
        verbose_name = "用户资料"
        verbose_name_plural = "用户资料"

class Follow(models.Model):
    """关注关系"""
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')
        verbose_name = "关注关系"
        verbose_name_plural = "关注关系"
    
    def __str__(self):
        return f"{self.follower.username} 关注 {self.following.username}"

class UserActivity(models.Model):
    """用户活动记录"""
    ACTIVITY_TYPES = [
        ('article_published', '发布文章'),
        ('comment_posted', '发表评论'),
        ('work_submitted', '提交作品'),
        ('event_attended', '参加活动'),
        ('report_downloaded', '下载报告'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "用户活动"
        verbose_name_plural = "用户活动"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()}" 