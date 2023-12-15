from django.urls import path

from . import views

urlpatterns = [
    path("registration", views.register_page, name="register"),
    path("login", views.login_page, name="login"),
    path("", views.home_page, name="home"),
    path("profile", views.profile_page, name="profile"),
    path('logout/', views.logout_view, name='logout'),
]