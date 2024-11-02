"""
URL configuration for fouritblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from blog.views import RegistrationView, BlogAPIList, UserAPIList, UserAPIUpdate, CommentAPIList, \
    CommentAPIDetailView, BlogAPIView, BlogAPIUpdate, BlogAPIDestroy, LikeAPIView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegistrationView.as_view(), name='register'),

    path('api/userlist/', UserAPIList.as_view()),
    path('api/userlist/<int:pk>/', UserAPIUpdate.as_view()),

    path('api/bloglist/', BlogAPIList.as_view()),
    path('api/blogview/<int:pk>/', BlogAPIView.as_view()),
    path('api/blogupdate/<int:pk>/', BlogAPIUpdate.as_view()),
    path('api/blogdestroy/<int:pk>/', BlogAPIDestroy.as_view()),

    path('api/commentlist/', CommentAPIList.as_view()),
    path('api/commentlist/<int:pk>/', CommentAPIDetailView.as_view()),
    path('api/commentlike/<int:pk>/', LikeAPIView.as_view()),
]
