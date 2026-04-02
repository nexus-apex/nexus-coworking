from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('coworkspaces/', views.coworkspace_list, name='coworkspace_list'),
    path('coworkspaces/create/', views.coworkspace_create, name='coworkspace_create'),
    path('coworkspaces/<int:pk>/edit/', views.coworkspace_edit, name='coworkspace_edit'),
    path('coworkspaces/<int:pk>/delete/', views.coworkspace_delete, name='coworkspace_delete'),
    path('coworkbookings/', views.coworkbooking_list, name='coworkbooking_list'),
    path('coworkbookings/create/', views.coworkbooking_create, name='coworkbooking_create'),
    path('coworkbookings/<int:pk>/edit/', views.coworkbooking_edit, name='coworkbooking_edit'),
    path('coworkbookings/<int:pk>/delete/', views.coworkbooking_delete, name='coworkbooking_delete'),
    path('coworkmembers/', views.coworkmember_list, name='coworkmember_list'),
    path('coworkmembers/create/', views.coworkmember_create, name='coworkmember_create'),
    path('coworkmembers/<int:pk>/edit/', views.coworkmember_edit, name='coworkmember_edit'),
    path('coworkmembers/<int:pk>/delete/', views.coworkmember_delete, name='coworkmember_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
