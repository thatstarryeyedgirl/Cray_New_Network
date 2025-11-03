from django.urls import path
from .views import RegisterView, LoginView, ForgotPasswordView, ResetPasswordView
urlpatterns = [
    # Define your URL patterns here
    path('register/', RegisterView.as_view(), name='chief_editor_register'),
    path('login/', LoginView.as_view(), name='chief_editor_login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='reset_password'), # uidb64 and token are part of the URL sent in the reset email
]
