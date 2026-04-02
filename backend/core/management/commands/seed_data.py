from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import CoworkSpace, CoworkBooking, CoworkMember
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusCoworking with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexuscoworking.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if CoworkSpace.objects.count() == 0:
            for i in range(10):
                CoworkSpace.objects.create(
                    name=f"Sample CoworkSpace {i+1}",
                    space_type=random.choice(["hot_desk", "dedicated_desk", "private_office", "meeting_room", "event_space"]),
                    capacity=random.randint(1, 100),
                    rate_per_day=round(random.uniform(1000, 50000), 2),
                    rate_per_month=round(random.uniform(1000, 50000), 2),
                    status=random.choice(["available", "occupied", "maintenance"]),
                    floor=f"Sample {i+1}",
                    amenities=f"Sample amenities for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 CoworkSpace records created'))

        if CoworkBooking.objects.count() == 0:
            for i in range(10):
                CoworkBooking.objects.create(
                    member_name=f"Sample CoworkBooking {i+1}",
                    space_name=f"Sample CoworkBooking {i+1}",
                    start_date=date.today() - timedelta(days=random.randint(0, 90)),
                    end_date=date.today() - timedelta(days=random.randint(0, 90)),
                    amount=round(random.uniform(1000, 50000), 2),
                    status=random.choice(["confirmed", "checked_in", "completed", "cancelled"]),
                    booking_type=random.choice(["hourly", "daily", "monthly"]),
                )
            self.stdout.write(self.style.SUCCESS('10 CoworkBooking records created'))

        if CoworkMember.objects.count() == 0:
            for i in range(10):
                CoworkMember.objects.create(
                    name=["Rajesh Kumar","Priya Sharma","Amit Patel","Deepa Nair","Vikram Singh","Ananya Reddy","Suresh Iyer","Meera Joshi","Karthik Rao","Fatima Khan"][i],
                    email=f"demo{i+1}@example.com",
                    phone=f"+91-98765{43210+i}",
                    company=["TechVision Pvt Ltd","Global Solutions","Pinnacle Systems","Nova Enterprises","CloudNine Solutions","MetaForge Inc","DataPulse Analytics","QuantumLeap Tech","SkyBridge Corp","Zenith Innovations"][i],
                    plan=random.choice(["day_pass", "weekly", "monthly", "annual"]),
                    status=random.choice(["active", "expired", "cancelled"]),
                    joined_date=date.today() - timedelta(days=random.randint(0, 90)),
                    credits=random.randint(1, 100),
                )
            self.stdout.write(self.style.SUCCESS('10 CoworkMember records created'))
