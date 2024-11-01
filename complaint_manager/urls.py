from django.urls import path

from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
path('user-complaints/', views.user_complaints_view, name='user_complaints'),
    path('user/<int:user_id>/', views.UserDetailView.as_view(), name='user_detail'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    #path('dashboard/', views.dashboard, name='dashboard'),
    #path('video/upload/', views.upload_video, name='upload_video'),
    #path('video/list/', views.video_list, name='video_list'),
    #path('chat/support/', views.chat_support, name='chat_support'),
    
path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
   path('register/', views.register_user, name='register'),
   path('upload/', views.UploadComplainView.as_view(), name='upload_complain'),
    path('list/', views.ComplainListView.as_view(), name='complain_list'),
    path('complain/<int:pk>/', views.ComplainDetailView.as_view(), name='complain_detail')



]

