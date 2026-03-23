from django.urls import path, include
from . import views

urlpatterns = [
    path("create/", views.CreateServerView.as_view()),
    path("join/public/<uuid:uid>/", views.JoinPubServerView.as_view()),
    path("join/invite/<uuid:code>/", views.JoinServerInviteView.as_view()),
    path("search/", views.SearchPubServerView.as_view()),
    
    path('<uuid:server_uid>/', include('chnls.urls')),
]
