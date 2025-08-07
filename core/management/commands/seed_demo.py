from django.core.management.base import BaseCommand
from django.utils import timezone
from wagtail.models import Site
from news.models import SectionIndexPage, ArticlePage, Channel
import random
from datetime import timedelta

# 生成示例数据：频道、栏目、文章
class Command(BaseCommand):
    help = "Seed demo channels/sections/articles for each site"
    
    def handle(self, *args, **kwargs):
        # 参考今日头条的频道分类
        channels = [
            "推荐",      # 首页推荐
            "热点",      # 热点新闻
            "科技",      # 科技资讯
            "财经",      # 财经新闻
            "体育",      # 体育新闻
            "娱乐",      # 娱乐八卦
            "军事",      # 军事新闻
            "国际",      # 国际新闻
            "社会",      # 社会新闻
            "健康",      # 健康养生
            "教育",      # 教育资讯
            "汽车",      # 汽车资讯
            "房产",      # 房产资讯
            "时尚",      # 时尚潮流
            "美食",      # 美食菜谱
            "旅游",      # 旅游攻略
            "游戏",      # 游戏资讯
            "数码",      # 数码产品
            "母婴",      # 母婴育儿
            "宠物",      # 宠物世界
            "历史",      # 历史人文
            "文化",      # 文化艺术
            "科学",      # 科学探索
            "环保",      # 环保生态
            "公益",      # 公益慈善
        ]
        
        # 创建频道
        for channel_name in channels:
            # 生成英文slug
            slug_map = {
                "推荐": "recommend",
                "热点": "hot",
                "科技": "tech",
                "财经": "finance",
                "体育": "sports",
                "娱乐": "entertainment",
                "军事": "military",
                "国际": "international",
                "社会": "society",
                "健康": "health",
                "教育": "education",
                "汽车": "auto",
                "房产": "real-estate",
                "时尚": "fashion",
                "美食": "food",
                "旅游": "travel",
                "游戏": "gaming",
                "数码": "digital",
                "母婴": "parenting",
                "宠物": "pets",
                "历史": "history",
                "文化": "culture",
                "科学": "science",
                "环保": "environment",
                "公益": "charity",
            }
            slug = slug_map.get(channel_name, channel_name.lower())
            Channel.objects.get_or_create(name=channel_name, slug=slug)
        
        # 为每个站点生成内容
        for site in Site.objects.all():
            root = site.root_page.specific
            sec_qs = root.get_children().type(SectionIndexPage).specific()
            sec = sec_qs.first()
            
            if not sec:
                sec = SectionIndexPage(title="新闻中心")
                root.add_child(instance=sec)
                sec.save_revision().publish()
            
            chs = list(Channel.objects.all())
            
            # 生成更多示例文章
            for i in range(20):
                # 根据频道生成更真实的标题
                channel = random.choice(chs)
                titles = {
                    "推荐": f"{site.site_name}推荐文章{i+1}",
                    "热点": f"热点新闻：{site.site_name}重要事件{i+1}",
                    "科技": f"科技前沿：{site.site_name}技术创新{i+1}",
                    "财经": f"财经资讯：{site.site_name}市场动态{i+1}",
                    "体育": f"体育新闻：{site.site_name}赛事报道{i+1}",
                    "娱乐": f"娱乐八卦：{site.site_name}明星动态{i+1}",
                    "军事": f"军事新闻：{site.site_name}国防动态{i+1}",
                    "国际": f"国际新闻：{site.site_name}全球视野{i+1}",
                    "社会": f"社会新闻：{site.site_name}民生关注{i+1}",
                    "健康": f"健康养生：{site.site_name}生活指南{i+1}",
                    "教育": f"教育资讯：{site.site_name}学习成长{i+1}",
                    "汽车": f"汽车资讯：{site.site_name}车市动态{i+1}",
                    "房产": f"房产资讯：{site.site_name}楼市分析{i+1}",
                    "时尚": f"时尚潮流：{site.site_name}潮流趋势{i+1}",
                    "美食": f"美食菜谱：{site.site_name}烹饪技巧{i+1}",
                    "旅游": f"旅游攻略：{site.site_name}旅行指南{i+1}",
                    "游戏": f"游戏资讯：{site.site_name}游戏动态{i+1}",
                    "数码": f"数码产品：{site.site_name}科技评测{i+1}",
                    "母婴": f"母婴育儿：{site.site_name}育儿经验{i+1}",
                    "宠物": f"宠物世界：{site.site_name}萌宠生活{i+1}",
                    "历史": f"历史人文：{site.site_name}历史探索{i+1}",
                    "文化": f"文化艺术：{site.site_name}文化传承{i+1}",
                    "科学": f"科学探索：{site.site_name}科学发现{i+1}",
                    "环保": f"环保生态：{site.site_name}绿色生活{i+1}",
                    "公益": f"公益慈善：{site.site_name}爱心行动{i+1}",
                }
                
                title = titles.get(channel.name, f"{site.site_name}文章{i+1}")
                
                a = ArticlePage(
                    title=title,
                    date=timezone.now() - timedelta(hours=i*2),
                    is_featured=(i % 4 == 0),  # 25%的文章设为特色
                    feature_rank=random.randint(0, 10)
                )
                sec.add_child(instance=a)
                a.save_revision().publish()
                
                # 为文章分配1-3个频道
                num_channels = random.choice([1, 2, 3])
                a.channels.add(*random.sample(chs, k=min(num_channels, len(chs))))
        
        self.stdout.write(
            self.style.SUCCESS(f"Demo data generated with {len(channels)} channels.")
        )
