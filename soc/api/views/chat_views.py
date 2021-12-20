from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from django.db.utils import IntegrityError
from django.core.paginator import Paginator, EmptyPage
from django.core.exceptions import ObjectDoesNotExist

from soc.api import serializers
from soc.api.services import accept_password_to_reg, ChatService
from soc.models import (
    Category,
    Post,
    Comment,
    User,
    GroupChat
)


def get_chat_by_id(chat_id: int) -> dict:
    chat = GroupChat.objects.filter(id=chat_id)
    return {
        "chat": chat.first(),
        "exists": chat.exists()
    }


class GroupChatListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request) -> Response:
        chats = GroupChat.objects.filter(users=request.user)
        serializer = serializers.GroupChatSerializer(chats, many=True)
        return Response(serializer.data)


class GroupChatDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, chat_id: int):
        chat_data = get_chat_by_id(chat_id)
        if not chat_data["exists"]:
            return Response({"message": f"Chat with id {chat_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        chat_service = ChatService(chat=chat_data['chat'], type_is_group=True)
        if not chat_service.is_user_member(user=request.user):
            return Response({"message": "You don't have permissions to see this chat."},
                            status=status.HTTP_403_FORBIDDEN)

        chat_serializer = serializers.GroupChatSerializer(chat_data['chat'])
        return Response(chat_serializer.data)

    def post(self, request, chat_id: int):
        chat_data = get_chat_by_id(chat_id)
        if not chat_data['exists']:
            return Response({"message": f"Chat with id {chat_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        chat_service = ChatService(chat=chat_data['chat'], type_is_group=True)
        if not chat_service.is_user_member(user=request.user):
            return Response({"message": "You don't have permissions to see this chat."},
                            status=status.HTTP_403_FORBIDDEN)

        message_serializer = serializers.GroupMessageSerializer(
            data={**request.data, **{"chat": chat_data['chat'].id}},
            context={"request": request}
        )

        if message_serializer.is_valid():
            message_serializer.save()
            return Response(message_serializer.data, status=status.HTTP_201_CREATED)

        return Response(message_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupMessageListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, chat_id: int):
        chat_data = get_chat_by_id(chat_id)
        if not chat_data["exists"]:
            return Response({"message": f"Chat with id {chat_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        chat_service = ChatService(chat=chat_data['chat'], type_is_group=True)
        if not chat_service.is_user_member(user=request.user):
            return Response({"message": "You don't have permissions to see this chat."},
                            status=status.HTTP_403_FORBIDDEN)

        page_number = request.query_params.get('page_number') or 1
        page_size = 15
        paginator = Paginator(chat_service.get_chat_messages(), page_size)

        try:
            serializer = serializers.GroupMessageSerializer(paginator.page(page_number), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except EmptyPage:
            return Response({}, status=status.HTTP_204_NO_CONTENT)


class GroupChatMemberListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, chat_id: int):
        chat_data = get_chat_by_id(chat_id)
        if not chat_data["exists"]:
            return Response({"message": f"Chat with id {chat_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        chat_service = ChatService(chat=chat_data['chat'])
        if not chat_service.is_user_member(user=request.user):
            return Response({"message": "You don't have permissions to see this chat."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.UserSerializer(chat_service.get_chat_members(), many=True)
        return Response(serializer.data)
