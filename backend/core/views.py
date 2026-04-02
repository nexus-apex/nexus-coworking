import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import CoworkSpace, CoworkBooking, CoworkMember


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['coworkspace_count'] = CoworkSpace.objects.count()
    ctx['coworkspace_hot_desk'] = CoworkSpace.objects.filter(space_type='hot_desk').count()
    ctx['coworkspace_dedicated_desk'] = CoworkSpace.objects.filter(space_type='dedicated_desk').count()
    ctx['coworkspace_private_office'] = CoworkSpace.objects.filter(space_type='private_office').count()
    ctx['coworkspace_total_rate_per_day'] = CoworkSpace.objects.aggregate(t=Sum('rate_per_day'))['t'] or 0
    ctx['coworkbooking_count'] = CoworkBooking.objects.count()
    ctx['coworkbooking_confirmed'] = CoworkBooking.objects.filter(status='confirmed').count()
    ctx['coworkbooking_checked_in'] = CoworkBooking.objects.filter(status='checked_in').count()
    ctx['coworkbooking_completed'] = CoworkBooking.objects.filter(status='completed').count()
    ctx['coworkbooking_total_amount'] = CoworkBooking.objects.aggregate(t=Sum('amount'))['t'] or 0
    ctx['coworkmember_count'] = CoworkMember.objects.count()
    ctx['coworkmember_day_pass'] = CoworkMember.objects.filter(plan='day_pass').count()
    ctx['coworkmember_weekly'] = CoworkMember.objects.filter(plan='weekly').count()
    ctx['coworkmember_monthly'] = CoworkMember.objects.filter(plan='monthly').count()
    ctx['recent'] = CoworkSpace.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def coworkspace_list(request):
    qs = CoworkSpace.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(space_type=status_filter)
    return render(request, 'coworkspace_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def coworkspace_create(request):
    if request.method == 'POST':
        obj = CoworkSpace()
        obj.name = request.POST.get('name', '')
        obj.space_type = request.POST.get('space_type', '')
        obj.capacity = request.POST.get('capacity') or 0
        obj.rate_per_day = request.POST.get('rate_per_day') or 0
        obj.rate_per_month = request.POST.get('rate_per_month') or 0
        obj.status = request.POST.get('status', '')
        obj.floor = request.POST.get('floor', '')
        obj.amenities = request.POST.get('amenities', '')
        obj.save()
        return redirect('/coworkspaces/')
    return render(request, 'coworkspace_form.html', {'editing': False})


@login_required
def coworkspace_edit(request, pk):
    obj = get_object_or_404(CoworkSpace, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.space_type = request.POST.get('space_type', '')
        obj.capacity = request.POST.get('capacity') or 0
        obj.rate_per_day = request.POST.get('rate_per_day') or 0
        obj.rate_per_month = request.POST.get('rate_per_month') or 0
        obj.status = request.POST.get('status', '')
        obj.floor = request.POST.get('floor', '')
        obj.amenities = request.POST.get('amenities', '')
        obj.save()
        return redirect('/coworkspaces/')
    return render(request, 'coworkspace_form.html', {'record': obj, 'editing': True})


@login_required
def coworkspace_delete(request, pk):
    obj = get_object_or_404(CoworkSpace, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/coworkspaces/')


@login_required
def coworkbooking_list(request):
    qs = CoworkBooking.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(member_name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'coworkbooking_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def coworkbooking_create(request):
    if request.method == 'POST':
        obj = CoworkBooking()
        obj.member_name = request.POST.get('member_name', '')
        obj.space_name = request.POST.get('space_name', '')
        obj.start_date = request.POST.get('start_date') or None
        obj.end_date = request.POST.get('end_date') or None
        obj.amount = request.POST.get('amount') or 0
        obj.status = request.POST.get('status', '')
        obj.booking_type = request.POST.get('booking_type', '')
        obj.save()
        return redirect('/coworkbookings/')
    return render(request, 'coworkbooking_form.html', {'editing': False})


@login_required
def coworkbooking_edit(request, pk):
    obj = get_object_or_404(CoworkBooking, pk=pk)
    if request.method == 'POST':
        obj.member_name = request.POST.get('member_name', '')
        obj.space_name = request.POST.get('space_name', '')
        obj.start_date = request.POST.get('start_date') or None
        obj.end_date = request.POST.get('end_date') or None
        obj.amount = request.POST.get('amount') or 0
        obj.status = request.POST.get('status', '')
        obj.booking_type = request.POST.get('booking_type', '')
        obj.save()
        return redirect('/coworkbookings/')
    return render(request, 'coworkbooking_form.html', {'record': obj, 'editing': True})


@login_required
def coworkbooking_delete(request, pk):
    obj = get_object_or_404(CoworkBooking, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/coworkbookings/')


@login_required
def coworkmember_list(request):
    qs = CoworkMember.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(plan=status_filter)
    return render(request, 'coworkmember_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def coworkmember_create(request):
    if request.method == 'POST':
        obj = CoworkMember()
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.phone = request.POST.get('phone', '')
        obj.company = request.POST.get('company', '')
        obj.plan = request.POST.get('plan', '')
        obj.status = request.POST.get('status', '')
        obj.joined_date = request.POST.get('joined_date') or None
        obj.credits = request.POST.get('credits') or 0
        obj.save()
        return redirect('/coworkmembers/')
    return render(request, 'coworkmember_form.html', {'editing': False})


@login_required
def coworkmember_edit(request, pk):
    obj = get_object_or_404(CoworkMember, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.phone = request.POST.get('phone', '')
        obj.company = request.POST.get('company', '')
        obj.plan = request.POST.get('plan', '')
        obj.status = request.POST.get('status', '')
        obj.joined_date = request.POST.get('joined_date') or None
        obj.credits = request.POST.get('credits') or 0
        obj.save()
        return redirect('/coworkmembers/')
    return render(request, 'coworkmember_form.html', {'record': obj, 'editing': True})


@login_required
def coworkmember_delete(request, pk):
    obj = get_object_or_404(CoworkMember, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/coworkmembers/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['coworkspace_count'] = CoworkSpace.objects.count()
    data['coworkbooking_count'] = CoworkBooking.objects.count()
    data['coworkmember_count'] = CoworkMember.objects.count()
    return JsonResponse(data)
