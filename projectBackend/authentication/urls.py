# authentication/urls.py
from django.urls import path
from .views import request_otp, verify_otp

# إذا عندك دالة login_view فعلاً في views.py خلّي السطر التالي،
# وإذا ما عندك login_view إحذف سطر اللوجن من urlpatterns تحت.
from . import views  # اختياري فقط إن كنت ستستخدم views.login_view

urlpatterns = [
    # إذا لديك login_view في authentication/views.py:
    # path("login/", views.login_view, name="login"),

    path("request-otp/", request_otp, name="request-otp"),
    path("verify-otp/", verify_otp, name="verify-otp"),
]
