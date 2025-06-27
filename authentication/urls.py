from django.urls import path
from . import views


urlpatterns=[
    path("",views.login_page, name="login"),
path("logout/",views.logout_page, name="logout"),
path("signup/",views.signup_page, name="signup"),
path('profile/', views.profile_view, name='profile'),
# path('user-activity/', views.user_activity_logs, name='user_activity_logs'),
path('verify-password/', views.verify_password, name='verify_password'),
    path("impersonate/<int:user_id>/", views.impersonate_user, name="impersonate_user"),
path("revert/", views.revert_impersonation, name="revert_impersonation"),
]