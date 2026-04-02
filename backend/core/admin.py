from django.contrib import admin
from .models import CoworkSpace, CoworkBooking, CoworkMember

@admin.register(CoworkSpace)
class CoworkSpaceAdmin(admin.ModelAdmin):
    list_display = ["name", "space_type", "capacity", "rate_per_day", "rate_per_month", "created_at"]
    list_filter = ["space_type", "status"]
    search_fields = ["name", "floor"]

@admin.register(CoworkBooking)
class CoworkBookingAdmin(admin.ModelAdmin):
    list_display = ["member_name", "space_name", "start_date", "end_date", "amount", "created_at"]
    list_filter = ["status", "booking_type"]
    search_fields = ["member_name", "space_name"]

@admin.register(CoworkMember)
class CoworkMemberAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "company", "plan", "created_at"]
    list_filter = ["plan", "status"]
    search_fields = ["name", "email", "phone"]
