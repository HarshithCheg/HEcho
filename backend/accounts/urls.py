from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view()),
    path('signin/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('friends/list/', views.FriendListView.as_view()),
    path('friends/incoming/', views.FriendIncListView.as_view()),
    path('friends/outgoing/', views.FriendOutListView.as_view()),
    path('friends/send/', views.FriendSendReqView.as_view()),
    path('friends/<uuid:uid>/reject/', views.FriendRejReqView.as_view()),
    path('friends/<uuid:uid>/accept/', views.FriendAccReqView.as_view()),
]
