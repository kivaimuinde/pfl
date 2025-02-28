from django.urls import path
from .views import users

app_name='core'

urlpatterns = [

    path("", users.home, name="home"),

    # Users URLs
    path("register/", users.register_user, name="register"),
    path("login/", users.login_user, name="login"),
    path("logout/", users.logout_user, name="logout"),
    path("reset-password/", users.reset_password, name="password_reset"),
    path("change-password/", users.change_password, name="change_password"),
    path("profile/", users.profile_view, name="profile"),
    path("profile/edit/", users.profile_update, name="profile_edit"),
    path("loggedout/reason/inactive/", users.logout_inactive_user, name="logout_inactive_user"),
]
