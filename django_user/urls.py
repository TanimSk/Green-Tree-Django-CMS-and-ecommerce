from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from django.views.generic import TemplateView

from core import urls as core_urls


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include(core_urls)),

    # Login and Logout
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='commons/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # User Page 
    path('user/', TemplateView.as_view(template_name='user.html'), name='user'),

    # Change Password
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='commons/change-password.html',
            success_url = '/'
        ),
        name='change_password'
    ),

    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='commons/password-reset/password_reset.html',
             subject_template_name='commons/password-reset/password_reset_subject.txt',
             email_template_name='commons/password-reset/password_reset_email.html',
             success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='commons/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='commons/password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='commons/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
