from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_view
from .import views


app_name = "users"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # path("registration/", views.registration, name="registration"),
    # path("profile/", views.profile, name="profile"),
    # path("password_change/", auth_view.PasswordChangeView.as_view(template_name="registration/password_change_form.html",
    #                                                             success_url="users:password_change_done"),
    #                                                             name="password_change"),
    # path("password_change_done/", auth_view.PasswordChangeDoneView.as_view(template_name="registration/password_change_done.html"),
    #                                                             name="password_change_done"),
    # path("password_reset/", auth_view.PasswordResetView.as_view(template_name="registration/password_reset_form.html",
    #                                                             email_template_name="users/password_reset_email.html",
    #                                                             success_url="users:password_reset_done"),
    #                                                             name="password_reset"),
    # path("password_reset_done/", auth_view.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
    #                                                             name="password_reset_done"),
    # path("password_reset_complete/", auth_view.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),
    #                                                             name="password_reset_complete"),
    # path("reset/<uidb64>/<token>/", auth_view.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html",
    #                                                             success_url="users:password_reset_complete"),
    #                                                             name="password_reset_confirm"),
]
