from django.urls import path

from . import views


urlpatterns = [
    path('user/find/<int:user_id>/', views.UserViewSet.as_view({"get": "retrieve"})),
    path('user/find/<str:username>/', views.UserViewSet.as_view({"get": "retrieve"})),
    path('user/find/<int:user_id>/friends/', views.UserFriendsAPIView.as_view()),
    path('user/find/<int:to_user>/friend_request/', views.FriendRequestViewSet.as_view(
        {"get": "retrieve", "post": "create",
         "delete": "destroy", "patch": "update"})),    
    path('user/find/<int:user_id>/request-notifications/', views.FriendRequestViewSet.as_view({"get": "list"})),

    path('user/register/', views.UserViewSet.as_view({"post": "create_registration_user"}), name="register-user"),
    path('user/is_auth/', views.UserViewSet.as_view({"get": "retrieve_current_user"}), name='current-user-data'),
    path('user/accept/<str:token>/', views.UserViewSet.as_view({"patch": "accept_registration_user"}), name="accept-user"),
    path('user/posts/<int:user_id>/', views.UserViewSet.as_view({"get": "list_of_user_posts"})),
    path('user/comments/<int:user_id>/', views.UserViewSet.as_view({"get": "list_of_user_comments"})),

]