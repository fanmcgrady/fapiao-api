"""fapiao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url

from home import views as home_views


urlpatterns = [
    # API
    url(r"^qr_api$", home_views.QR_API),
    url(r"^type_api$", home_views.Type_API),
    url(r"^detect_api$", home_views.Detect_API),

    # 批量上传
    url(r"^getFileList$", home_views.getFileList),

    url(r"^$", home_views.index),

    url(r"^type$", home_views.testType),

    # 多票面检测
    url(r"^multi$", home_views.multi),

    # 统一入口
    url(r"^detect$", home_views.detect),
    url(r"^ocrForSpecVat$", home_views.ocrForSpecVat),
]

