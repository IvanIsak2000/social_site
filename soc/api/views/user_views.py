import serializer as serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from django.core.exceptions import ObjectDoesNotExist

from soc.api import serializers
from soc.api.services import accept_password_to_reg, UserService


class UserJwtAPIView(APIView):
    """API View to get data about current user."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailAPIView(APIView):
    """API View to get data about some user by his some data."""
    def get(self, request, username: str = None, user_id: int = None):
        user = UserService.get_user(user_id=user_id, username=username)
        if not user:
            return Response({"error": "User not found with given data."}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegistrationUserAPIView(APIView):
    """API View for registration a user"""
    def post(self, request):
        serializer = serializers.RegistrationUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AcceptUserAPIView(APIView):
    """API View for accepting user by his token."""
    def get(self, request, token: str):
        try:
            accept_password_to_reg(token=token)
        except (ObjectDoesNotExist, NameError):
            return Response({"message": "Token doesnt exists."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Accepted successfully."}, status=status.HTTP_200_OK)


class UserDetailPostAPIView(APIView):
    """API View to get all user posts."""
    def get(self, request, user_id: int) -> Response:
        user_service = UserService(user_id)
        posts = user_service.get_user_posts()
        serializer = serializers.PostSerializer(posts, many=True)
        if not posts:
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailCommentAPIView(APIView):
    """API View to get all user comments."""
    def get(self, request, user_id: int):
        user_service = UserService(user_id)
        comments = user_service.get_user_comments()
        serializer = serializers.CommentSerializer(comments, many=True)
        if not comments:
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserFriendsAPIView(APIView):
    """API View to get all user friends."""
    def get(self, request, user_id: int) -> Response:
        user_service = UserService(user_id)
        friends = user_service.get_user_friends()
        serializer = serializers.UserSerializer(friends, many=True)
        return Response(serializer.data)


class FriendRequestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, to_user: int):
        user_service = UserService(request.user.id)
        to_user_object = UserService.get_user(user_id=to_user)

        if not to_user_object:
            return Response({"message": "User with this id doesnt exists."}, status=status.HTTP_404_NOT_FOUND)

        if not user_service.is_friend_request_exists(to_user_object):
            return Response({"message": "Friend Request with this data doesnt exists."}, status=status.HTTP_404_NOT_FOUND)

        friend_request = UserService.get_friend_request(request.user, to_user_object)
        if not friend_request:
            return Response({"message": "Bad request."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.FriendRequestSerializer(friend_request)
        return Response(serializer.data)

    def post(self, request, to_user: int):
        user_service = UserService(request.user.id)
        data = user_service.create_friend_request(to_user)

        if data["error"]:
            return Response({"message": data["error"]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.FriendRequestSerializer(data["instanse"])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
