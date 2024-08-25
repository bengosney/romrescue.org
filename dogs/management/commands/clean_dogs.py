# Standard Library
from datetime import datetime, timedelta

# Django
from django.core.management.base import BaseCommand

# First Party
from dogs.models import Dog


class Command(BaseCommand):
    help = "Remove adopted dog that haven't been updated in a while"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days-to-keep",
            action="store",
            dest="last_n_days",
            default=365,
            type=int,
            help="Days to keep dogs",
        )

    def handle(self, *args, **options):
        delta = datetime.now() - timedelta(days=options.get("last_n_days", 365))
        dogs = Dog.objects.filter(dogStatus=Dog.STATUS_FOUND, modified__lt=delta)
        print(f"Cleaning {len(dogs)} dogs")
        dogs.delete()
