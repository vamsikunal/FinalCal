from django.contrib import admin
from django.urls import path
from app import views

# Template urls
app_name = 'app'

urlpatterns = [
   path('register/', views.register, name='register'),
   path('', views.base.as_view(), name='base'),
   path('login/', views.user_login, name='login'),
   path('about/', views.about.as_view(), name='about'),
   path('logout/', views.user_logout, name='logout'),
   path('event/', views.create_event, name='event'),
   path('home/', views.CalanderView, name='calendar'),
   path('event_detail/<int:event_id>/', views.event_details, name='event_detail'),
   path('calendar2', views.calendar2, name='calendar2')
]
