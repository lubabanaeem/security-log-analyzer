from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", views.home, name="home"),
    path("alert/<int:alert_id>/", views.alert_detail, name="alert_detail"),
    path("export/<int:upload_id>/", views.export_report, name="export_report"),
]
