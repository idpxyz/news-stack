from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from wagtail.models import Site, GroupSitePermission
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class Command(BaseCommand):
    help = "Setup site-specific permissions for multi-site management"
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--site',
            type=str,
            help='Specific site hostname to setup permissions for'
        )
        parser.add_argument(
            '--user',
            type=str,
            help='Username to assign site permissions to'
        )
        parser.add_argument(
            '--role',
            type=str,
            choices=['admin', 'editor', 'publisher', 'moderator'],
            help='Role to assign to the user'
        )
        parser.add_argument(
            '--list-sites',
            action='store_true',
            help='List all available sites'
        )
        parser.add_argument(
            '--list-users',
            action='store_true',
            help='List all users and their site permissions'
        )
    
    def handle(self, *args, **options):
        if options['list_sites']:
            self.list_sites()
            return
        
        if options['list_users']:
            self.list_users()
            return
        
        if options['site'] and options['user'] and options['role']:
            self.assign_site_permission(
                options['site'], 
                options['user'], 
                options['role']
            )
        else:
            self.setup_default_permissions()
    
    def list_sites(self):
        """列出所有可用站点"""
        sites = Site.objects.all()
        if not sites.exists():
            self.stdout.write(self.style.WARNING("No sites found."))
            return
        
        self.stdout.write(self.style.SUCCESS("Available sites:"))
        for site in sites:
            self.stdout.write(f"  - {site.hostname}:{site.port} ({site.site_name})")
    
    def list_users(self):
        """列出所有用户及其站点权限"""
        users = User.objects.filter(is_active=True)
        if not users.exists():
            self.stdout.write(self.style.WARNING("No active users found."))
            return
        
        self.stdout.write(self.style.SUCCESS("Users and their site permissions:"))
        for user in users:
            self.stdout.write(f"\n👤 {user.username} ({user.get_full_name() or 'No name'})")
            
            # 检查超级用户权限
            if user.is_superuser:
                self.stdout.write("  🔑 Superuser (all permissions)")
                continue
            
            # 检查全局权限
            if user.is_staff:
                self.stdout.write("  👨‍💼 Staff user")
            
            # 检查站点特定权限
            site_permissions = GroupSitePermission.objects.filter(
                group__user=user
            ).select_related('site', 'permission', 'group')
            
            if site_permissions.exists():
                for sp in site_permissions:
                    self.stdout.write(
                        f"  🌐 {sp.site.hostname}:{sp.site.port} - "
                        f"{sp.permission.codename} (via {sp.group.name})"
                    )
            else:
                self.stdout.write("  ❌ No site-specific permissions")
    
    def assign_site_permission(self, hostname, username, role):
        """为特定用户分配站点权限"""
        try:
            # 获取站点
            site = Site.objects.get(hostname=hostname)
        except Site.DoesNotExist:
            raise CommandError(f"Site '{hostname}' not found")
        
        try:
            # 获取用户
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f"User '{username}' not found")
        
        # 定义角色权限
        role_permissions = {
            'admin': [
                'add_page', 'change_page', 'delete_page', 'publish_page',
                'add_site', 'change_site', 'delete_site',
                'add_collection', 'change_collection', 'delete_collection'
            ],
            'editor': [
                'add_page', 'change_page', 'publish_page'
            ],
            'publisher': [
                'change_page', 'publish_page'
            ],
            'moderator': [
                'change_page', 'publish_page'
            ]
        }
        
        permissions = role_permissions.get(role, [])
        if not permissions:
            raise CommandError(f"Invalid role '{role}'")
        
        # 创建或获取用户组
        group_name = f"{site.site_name}_{role.title()}"
        group, created = Group.objects.get_or_create(name=group_name)
        
        if created:
            self.stdout.write(f"Created group: {group_name}")
        
        # 分配权限
        for perm_name in permissions:
            try:
                # 尝试获取页面权限
                perm = Permission.objects.get(
                    codename=perm_name,
                    content_type__app_label='wagtailcore'
                )
            except Permission.DoesNotExist:
                try:
                    # 尝试获取站点权限
                    perm = Permission.objects.get(
                        codename=perm_name,
                        content_type__model='site'
                    )
                except Permission.DoesNotExist:
                    try:
                        # 尝试获取集合权限
                        perm = Permission.objects.get(
                            codename=perm_name,
                            content_type__model='collection'
                        )
                    except Permission.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f"Permission '{perm_name}' not found, skipping")
                        )
                        continue
            
            # 创建站点特定权限
            site_perm, created = GroupSitePermission.objects.get_or_create(
                group=group,
                site=site,
                permission=perm
            )
            
            if created:
                self.stdout.write(f"  ✅ Added {perm_name} permission")
        
        # 将用户添加到组
        user.groups.add(group)
        
        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Assigned {role} role to {username} for site {hostname}"
            )
        )
    
    def setup_default_permissions(self):
        """设置默认的站点权限结构"""
        sites = Site.objects.all()
        if not sites.exists():
            self.stdout.write(self.style.WARNING("No sites found. Please create sites first."))
            return
        
        # 为每个站点创建权限组
        for site in sites:
            self.stdout.write(f"\n🔧 Setting up permissions for {site.hostname}:{site.port}")
            
            # 创建站点管理员组
            admin_group, _ = Group.objects.get_or_create(
                name=f"{site.site_name}_管理员"
            )
            
            # 创建站点编辑组
            editor_group, _ = Group.objects.get_or_create(
                name=f"{site.site_name}_编辑者"
            )
            
            # 创建站点发布组
            publisher_group, _ = Group.objects.get_or_create(
                name=f"{site.site_name}_发布者"
            )
            
            # 定义权限
            admin_permissions = [
                'add_page', 'change_page', 'delete_page', 'publish_page',
                'add_site', 'change_site', 'delete_site'
            ]
            
            editor_permissions = [
                'add_page', 'change_page', 'publish_page'
            ]
            
            publisher_permissions = [
                'change_page', 'publish_page'
            ]
            
            # 分配权限
            self._assign_permissions_to_group(site, admin_group, admin_permissions)
            self._assign_permissions_to_group(site, editor_group, editor_permissions)
            self._assign_permissions_to_group(site, publisher_group, publisher_permissions)
        
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅ Setup complete! Created permission groups for {sites.count()} sites.\n"
                f"Use --list-users to see current permissions.\n"
                f"Use --site <hostname> --user <username> --role <role> to assign specific permissions."
            )
        )
    
    def _assign_permissions_to_group(self, site, group, permission_names):
        """为组分配权限"""
        for perm_name in permission_names:
            try:
                # 尝试获取页面权限
                perm = Permission.objects.get(
                    codename=perm_name,
                    content_type__app_label='wagtailcore'
                )
            except Permission.DoesNotExist:
                try:
                    # 尝试获取站点权限
                    perm = Permission.objects.get(
                        codename=perm_name,
                        content_type__model='site'
                    )
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f"  ⚠️  Permission '{perm_name}' not found")
                    )
                    continue
            
            # 创建站点特定权限
            GroupSitePermission.objects.get_or_create(
                group=group,
                site=site,
                permission=perm
            )
        
        self.stdout.write(f"  ✅ Created {group.name} group") 