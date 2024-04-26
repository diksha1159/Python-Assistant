from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='home'),  # Map the root URL to the index view
    path('about', views.about, name='about'),
    path('services', views.services, name='services'),
    path('contact', views.contact, name='contact'),
    path('summary', views.summary, name='summary'),
 
    path('signup/', views.SignupPage, name='signup'),  # Changed URL pattern
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutPage, name='logout'),
]
