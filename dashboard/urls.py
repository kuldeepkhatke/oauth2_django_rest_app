from django.contrib import admin
from django.urls import path
from . import views
from .views import TaskView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'task_api', TaskView, basename='task_api')

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login_view'),
    path('login_api/', views.LoginAPIView.as_view(), name='login_api'),
    path('register/', views.register_view, name='register_view'),
    path('register_api/', views.RegisterAPIView.as_view(), name='register_api'),
    path('user_profile/', views.UserProfile.as_view(), name='user_profile'),
    # path('task_api/', views.TaskView, name='task_api')
]

urlpatterns += router.urls