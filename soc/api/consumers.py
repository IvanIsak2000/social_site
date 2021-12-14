from jwt import decode as jwt_decode
import json
from typing import Union

from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser
from django.conf import settings

from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from . import serializers
from soc.models import Chat, Message, User
from soc.api.services import ChatService


class GroupChatConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def get_chat(self, chat_id: int) -> Union[None or Chat]:
        return Chat.objects.filter(id=chat_id).first()

    @database_sync_to_async
    def get_user(token: str) -> Union[User or AnonymousUser]:
        if not token or token == b'null':
            return AnonymousUser()

        try:
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            return AnonymousUser()

        decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        try:
            return User.objects.get(id=decoded_data['user_id'])
        except ObjectDoesNotExist:
            return AnonymousUser()

    async def connect(self):
        chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = 'group_chat_%s' % chat_id

        chat = await self.get_chat(chat_id)
        if not chat:
            raise ObjectDoesNotExist("Chat doesn't exists.")

        chat_service = ChatService(chat)

        if not await sync_to_async(chat_service.is_user_member)(self.scope['user']):
            raise PermissionDenied("You are not member of this chat.")

        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):

        text_data_json = json.loads(text_data)

        await self.channel_layer.group_send(
            self.chat_group_name,
            {**text_data_json}
        )

    async def send_message(self, event):
        await self.send(text_data=json.dumps(event['data']))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )
