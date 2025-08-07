from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Create user groups for content management workflow."
    
    def handle(self, *args, **kwargs):
        # Create user groups for content management
        editors, _ = Group.objects.get_or_create(name="编辑者")
        publishers, _ = Group.objects.get_or_create(name="发布者")
        moderators, _ = Group.objects.get_or_create(name="审核者")
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Created user groups: {editors.name}, {publishers.name}, {moderators.name}"
            )
        )
