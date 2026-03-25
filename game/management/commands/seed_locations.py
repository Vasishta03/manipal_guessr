from django.core.management.base import BaseCommand
from game.models import Location


MANIPAL_LOCATIONS = [
    {
        "name": "MIT Main Gate",
        "description": "The main entrance to Manipal Institute of Technology, one of the most iconic spots on campus.",
        "latitude": 13.34934,
        "longitude": 74.79234,
        "hint": "You pass through here every day.",
    },
    {
        "name": "End Point",
        "description": "The famous viewpoint at the edge of Manipal, offering a stunning view of the Udupian landscape.",
        "latitude": 13.36660,
        "longitude": 74.78370,
        "hint": "Best sunset views in Manipal.",
    },
    {
        "name": "Manipal Lake",
        "description": "The serene lake in the heart of Manipal town, a popular hangout for students.",
        "latitude": 13.35030,
        "longitude": 74.77920,
        "hint": "Water body near the town centre.",
    },
    {
        "name": "MIT Library",
        "description": "The central library of MIT Manipal, where most of the academic hustle happens.",
        "latitude": 13.35240,
        "longitude": 74.79160,
        "hint": "Biggest building where books live.",
    },
    {
        "name": "Tiger Circle",
        "description": "The famous landmark roundabout with the tiger statue, a meeting point for students.",
        "latitude": 13.34430,
        "longitude": 74.79170,
        "hint": "Look for the big cat.",
    },
    {
        "name": "KMC Hospital",
        "description": "Kasturba Medical College Hospital, the major medical facility on the Manipal campus.",
        "latitude": 13.35680,
        "longitude": 74.79040,
        "hint": "The big healthcare complex.",
    },
    {
        "name": "Manipal Food Court",
        "description": "The central food court area where students gather between classes.",
        "latitude": 13.35100,
        "longitude": 74.79050,
        "hint": "Where hunger gets solved.",
    },
    {
        "name": "Academic Block 1 - MIT",
        "description": "The first academic block of MIT, home to lectures and labs.",
        "latitude": 13.35200,
        "longitude": 74.79300,
        "hint": "First stop for first years.",
    },
    {
        "name": "Manipal Centre",
        "description": "The commercial hub of Manipal with shops, cafes, and amenities for students.",
        "latitude": 13.34500,
        "longitude": 74.79420,
        "hint": "Go here when you need to shop.",
    },
    {
        "name": "Valley View",
        "description": "A scenic spot overlooking the valley, popular among students for evening walks.",
        "latitude": 13.35730,
        "longitude": 74.78040,
        "hint": "High up, great view.",
    },
    {
        "name": "Manipal Bus Stop (Town)",
        "description": "The main bus stop in Manipal town, connecting students to Udupi and beyond.",
        "latitude": 13.34700,
        "longitude": 74.79100,
        "hint": "Where the journey begins.",
    },
    {
        "name": "Manipal Golf Course",
        "description": "The green golf course that sits inside the Manipal campus.",
        "latitude": 13.35500,
        "longitude": 74.78500,
        "hint": "Fore! Green grass and fairways.",
    },
]


class Command(BaseCommand):
    help = 'Seed the database with sample Manipal locations'

    def handle(self, *args, **kwargs):
        created = 0
        skipped = 0
        for loc_data in MANIPAL_LOCATIONS:
            obj, was_created = Location.objects.get_or_create(
                name=loc_data['name'],
                defaults={
                    'description': loc_data['description'],
                    'latitude': loc_data['latitude'],
                    'longitude': loc_data['longitude'],
                    'hint': loc_data.get('hint', ''),
                    'is_active': True,
                }
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"  Created: {obj.name}"))
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! Created {created} locations, skipped {skipped} existing."
        ))
        self.stdout.write(self.style.WARNING(
            "\n📸 Don't forget to add images via the Django admin panel at /admin/"
        ))
