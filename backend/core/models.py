from django.db import models

class CoworkSpace(models.Model):
    name = models.CharField(max_length=255)
    space_type = models.CharField(max_length=50, choices=[("hot_desk", "Hot Desk"), ("dedicated_desk", "Dedicated Desk"), ("private_office", "Private Office"), ("meeting_room", "Meeting Room"), ("event_space", "Event Space")], default="hot_desk")
    capacity = models.IntegerField(default=0)
    rate_per_day = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    rate_per_month = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=[("available", "Available"), ("occupied", "Occupied"), ("maintenance", "Maintenance")], default="available")
    floor = models.CharField(max_length=255, blank=True, default="")
    amenities = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class CoworkBooking(models.Model):
    member_name = models.CharField(max_length=255)
    space_name = models.CharField(max_length=255, blank=True, default="")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=[("confirmed", "Confirmed"), ("checked_in", "Checked In"), ("completed", "Completed"), ("cancelled", "Cancelled")], default="confirmed")
    booking_type = models.CharField(max_length=50, choices=[("hourly", "Hourly"), ("daily", "Daily"), ("monthly", "Monthly")], default="hourly")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.member_name

class CoworkMember(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=255, blank=True, default="")
    company = models.CharField(max_length=255, blank=True, default="")
    plan = models.CharField(max_length=50, choices=[("day_pass", "Day Pass"), ("weekly", "Weekly"), ("monthly", "Monthly"), ("annual", "Annual")], default="day_pass")
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("expired", "Expired"), ("cancelled", "Cancelled")], default="active")
    joined_date = models.DateField(null=True, blank=True)
    credits = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
