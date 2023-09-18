from django.urls import path,include
from Patients.views import (PatientRegistrationView,PatientLoginView,VerifyotpView,
                            OtpResetPasswordView,PasswordResetView,PatientView,PatientUpdateView,ResendOtpView
)
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('registration' ,PatientRegistrationView.as_view(),name='register-patient'),
    path('verify-email',VerifyotpView.as_view(),name='verify-email'),
    path('login',PatientLoginView.as_view(),name='login-patient'),
    path('otp-send',OtpResetPasswordView.as_view(),name='otp-sent'),
    path('reset-password',PasswordResetView.as_view(),name='reset-password'),
    path('',PatientView.as_view(),name='patient-user'),
    path('<int:pk>',PatientUpdateView.as_view(),name='patient-update'),
    path('resend-otp',ResendOtpView.as_view(),name='resend-otp')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)