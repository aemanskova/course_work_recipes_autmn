from django.contrib.auth.views import LoginView
from django.urls import path

from users.views import UserList, UserDetail, CurrentUser, UsersListView, UserDetailView, SignupView, ProfileView

app_name = 'users'

urlpatterns = [
    # path("users/", UserList.as_view()),
    # path("users/<int:pk>/", UserDetail.as_view()),
    # path("users/current/", CurrentUser.as_view()),
    path('login/',
         LoginView.as_view(
             template_name='users/login.html'),
         name='login'),
    path('users/',
         UsersListView.as_view(),
         name='users_list'),
    path('users/<int:id>/',
         UserDetailView.as_view(),
         name='user_detail'),

    path('signup/',
         SignupView.as_view(),
         name='signup'),
    path('profile/',
         ProfileView.as_view(),
         name='profile'),
]
