from django.urls import path
from .views import users
urlpatterns = [
    # Users URLs
    path("register/", users.register_user, name="register"),
    path("login/", users.login_user, name="login"),
    path("logout/", users.logout_user, name="logout"),
    path("reset-password/", users.reset_password, name="reset_password"),
    path("change-password/", users.change_password, name="change_password"),
    path("profile/", users.profile_view, name="profile"),
    path("profile/edit/", users.profile_update, name="profile_edit"),
]
