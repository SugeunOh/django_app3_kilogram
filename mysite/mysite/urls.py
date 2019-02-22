"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from kilogram import views  as kilogram_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', kilogram_views.IndexView.as_view(), name='root'),
    url(r'^admin/', admin.site.urls),
    url(r'^kilogram/', include('kilogram.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')), # 인증관련된 views는 미리 정의가 되어있어 url만 추가해주면 됨.
    url(r'^accounts/signup$', kilogram_views.CreateUserView.as_view(), name="signup"),                # 회원가입 화면
    url(r'^accounts/signup/done$', kilogram_views.RegisteredView.as_view(), name="create_user_done"), # 회원가입이 완료된 화면
]

# 첫번째 인자 : 어떤 URL을 정적으로 추가할래?, 두번쨰 인자 : 실제는 어디에 있는데?
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


