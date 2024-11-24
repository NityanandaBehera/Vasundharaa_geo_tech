from django.urls import path
from . import views

urlpatterns = [
    
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Organization Management URLs
    path('organizations/', views.organization_list, name='organization_list'),
    path('organizations/create/', views.organization_create, name='organization_create'),
    path('organizations/<int:pk>/update/', views.organization_update, name='organization_update'),
    path('organizations/<int:pk>/delete/', views.organization_delete, name='organization_delete'),
    path('organizations/<int:pk>/', views.organization_detail, name='organization_detail'),
    
    # User Management URLs
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/update/', views.user_update, name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),

    # Role Assignment URL
    path('users/<int:pk>/assign-role/', views.assign_role, name='assign_role'),
]


