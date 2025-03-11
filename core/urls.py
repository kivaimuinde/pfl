from django.urls import path
from .views import users, departments

app_name='core'

urlpatterns = [

    path("", users.home, name="home"),
    path("dashboard/", users.dashboard, name="dashboard"),

    # Users URLs
    path("register/", users.register_user, name="register"),
    path("login/", users.login_user, name="login"),
    path("logout/", users.logout_user, name="logout"),
    path("reset-password/", users.reset_password, name="password_reset"),
    path("change-password/", users.change_password, name="change_password"),
    path("profile/", users.profile_view, name="profile"),
    path("profile/edit/", users.profile_update, name="profile_edit"),
    path("loggedout/reason/inactive/", users.logout_inactive_user, name="logout_inactive_user"),



    path("profile/all/", users.user_list, name="user_list"),
    path('profiles/<int:user_id>/details', users.user_detail, name='user_detail'),
    path('users/<int:user_id>/edit/profile/', users.edit_user_profile, name='edit_user_profile'),

    path("users/action/<int:user_id>/deactivate", users.deactivate_user, name="deactivate_user"),
    path("users/action/<int:user_id>/activate", users.activate_user, name="activate_user"),


     # Department URLs

    
    path('departments/', departments.department_list, name='department_list'),
    path('departments/<int:pk>/details', departments.department_detail, name='department_detail'),
    path('departments/add/new/', departments.department_create, name='department_create'),
    path('departments/<int:pk>/details/edit/', departments.department_update, name='department_update'),
    path('departments/<int:pk>/delete/', departments.department_delete, name='department_delete'),
]
