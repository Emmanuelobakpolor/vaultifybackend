from django.core.management.base import BaseCommand
from backend_file.api.models import Provider, Admin

class Command(BaseCommand):
    help = 'Fix Provider records with null admin by assigning a default admin'

    def handle(self, *args, **kwargs):
        # Get or create a default admin to assign
        default_admin, created = Admin.objects.get_or_create(
            adminEmail='defaultadmin@example.com',
            defaults={
                'adminName': 'Default Admin',
                'adminRole': 'Super-admin',
                'adminPassword': 'defaultpassword'  # You may want to hash this properly
            }
        )
        # Find providers with null admin
        providers_without_admin = Provider.objects.filter(admin__isnull=True)
        count = providers_without_admin.count()
        if count == 0:
            self.stdout.write(self.style.SUCCESS('No Provider records with null admin found.'))
            return
        # Assign default admin to these providers
        providers_without_admin.update(admin=default_admin)
        self.stdout.write(self.style.SUCCESS(f'Assigned default admin to {count} Provider records.'))
