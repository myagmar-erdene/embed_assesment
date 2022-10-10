from django.urls import path, include
from rest_framework.authtoken import views

from .views import \
    RegisterView, \
    LoginView, \
    LogoutView, \
    UserProfileView, \
    CountriesView, \
    CitiesView, \
    InterestsView, \
    UserInterestsView, \
    PostsView, \
    UserSubscriptionsView, \
    ManageUserSubscriptionsView, \
    UserSubscribersView, \
    UserProfileDetailsView, \
    UsersView, \
    TopTwentyUsersView


urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('my-profile/', UserProfileView.as_view(), name='my-profile'),
    path('countries/', CountriesView.as_view(), name='countries'),
    path('cities/', CitiesView.as_view(), name='cities'),
    path('interests/', InterestsView.as_view(), name='interests'),
    path('user-interests/', UserInterestsView.as_view(), name='user-interests'),
    path('user-interests/<int:user_id>/', UserInterestsView.as_view(),
         name='user-interests'),
    path('posts/', PostsView.as_view(), name='posts'),
    path('my-subscriptions/', UserSubscriptionsView.as_view(),
         name='my-subscriptions'),
    path('my-subscriptions-manage/<int:subscribed_to_user_id>/',
         ManageUserSubscriptionsView.as_view(),
         name='my-subscriptions-manage'),
    path('my-subscribers/', UserSubscribersView.as_view(),
         name='my-subscribers'),
    path('my-profile-details/', UserProfileDetailsView.as_view(),
         name='my-profile-details/'),
    path('users/', UsersView.as_view(), name='users'),
    path('top-twenty-users/', TopTwentyUsersView.as_view(),
         name='top-twenty-users')
]

urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]
