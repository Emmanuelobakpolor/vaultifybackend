from django.core.management.base import BaseCommand
from api.models import Service

class Command(BaseCommand):
    help = 'Seed the Service table with fixed categories'

    def handle(self, *args, **kwargs):
        categories = [
            "Cleaning Service",
            "Plumbing Service",
            "Electrical Service",
            "Pest Control",
            "Appliance Repair",
            "Landscaping/Gardening",
            "Security Service",
            "General Maintenance",
            "Fire Fighters",
        ]
        for category in categories:
            service, created = Service.objects.get_or_create(name=category)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created service: {category}'))
            else:
                self.stdout.write(f'Service already exists: {category}')
