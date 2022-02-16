import json
import uuid
from typing import Union

from django.contrib.auth.models import Group
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.response import Response

from server.settings import BASE_DIR
from user_app.models import User


class UserAPITestCase(APITestCase):
    json_users_path = BASE_DIR / 'user_app/test_data/user_data.json'

    def setUp(self):
        f = open(self.json_users_path, 'r')
        self.users_dict = json.loads(f.read())
        Group.objects.create(name='Пользователь')

    def _create_users(self, json_users: dict) -> list[Response]:
        url = reverse('register-user')
        responses = [self.client.post(url, user_data, format='json') for user_data in json_users]
        return responses

    def _accept_user(self, token) -> Response:
        url = reverse('accept-user', args=[token])
        response = self.client.patch(url)
        return response

    def _accept_all_users(self, users: list[User]) -> None:
        for user in users:
            user.is_active = True
            user.save()

    def _login_user(self, username=None, password=None) -> Response:
        client = APIClient()
        url = reverse("token_obtain_pair")
        if username and password:
            data = {"username": username, "password": password}
        else:
            data = {}

        response = client.post(url, data=data, format='json')
        return response

    def _login_many_users(self, users: list[User]):
        responses = []
        for user in users:
            response = self._login_user(user.username, "the_same_password")
            responses.append({
                user.id: {
                    "data": response.json(),
                    "status_code": response.status_code
                }
            })

        return responses

    def _get_current_user_response(self, jwt: str) -> Response:
        url = reverse('current-user-data')
        client = APIClient()
        response = client.get(url, data=None, follow=False, HTTP_AUTHORIZATION=f'Bearer {jwt}')
        return response

    def test_creating_users(self):
        responses = self._create_users(self.users_dict)
        statuses = [response.status_code for response in responses]
        users = User.objects.all()

        self.assertEqual(len(responses)-4, users.count())
        self.assertEqual(statuses[5:], [status.HTTP_400_BAD_REQUEST for _ in range(4)])

        unique_statuses = list(set(statuses))
        unique_statuses.remove(400)
        self.assertEqual([unique_statuses[0], len(unique_statuses) == 1], [status.HTTP_201_CREATED, True])

    def test_accepting_users(self):
        self._create_users(self.users_dict)

        users = User.objects.all()

        is_active_list = [user.is_active for user in users]
        wrong_requests_statuses = [self._accept_user(uuid.uuid1()).status_code for _ in range(5)]
        correct_requests_statuses = [self._accept_user(user.acceptauthtoken.token).status_code for user in users]

        self.assertEqual(is_active_list, [0 for _ in range(5)])
        self.assertEqual(wrong_requests_statuses, [404 for _ in range(5)])
        self.assertEqual(correct_requests_statuses, [200 for _ in range(5)])

    def test_login_users(self):
        self._create_users(self.users_dict)
        users = User.objects.all()
        self._accept_all_users(users)

        worst_response1 = self._login_user('Invalid User', 'invalid_password')
        worst_response2 = self._login_user()
        correct_responses = self._login_many_users(users)

        self.assertEqual(worst_response1.status_code, 401)
        self.assertIn('detail', worst_response1.json())

        self.assertEqual(worst_response2.status_code, 400)
        self.assertEqual('username' in worst_response2.json() and 'password' in worst_response2.json(), True)

        self.assertEqual(len(correct_responses), len(users))

        for response in correct_responses:
            for user_id, value in response.items():
                response = self._get_current_user_response(value['data']['access'])

                self.assertEqual(len(response.json()), 6)
                self.assertEqual(response.json()['id'], user_id)
                self.assertEqual(response.status_code, 200)

    def test_searching_user(self):
        self._create_users(self.users_dict)
        users = User.objects.all()
        self._accept_all_users(users)
