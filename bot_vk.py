import random
import requests

import user_settings


class BotVK:
    def __init__(self, user_token, group_token):
        self.user_token = user_token
        self.group_token = group_token

    def write_msg(self, user_id, message='empty message', attachment=''):
        """Функция отправки сообщения пользователю"""

        info_resp = requests.get(
            'https://api.vk.com/method/messages.send',
            params={
                'random_id': random.randrange(10 ** 7),
                'access_token': self.group_token,
                'v': 5.131,
                'user_id': user_id,
                'message': message,
                'attachment': attachment,
                #                 'keyboard': {}
            }
        )
        return info_resp

    def asking_question_and_get_answer_from_user(self, user_id, message='empty message', attachment='', flag_request=False):
        self.write_msg()
        self.checking_user_message()

    def get_conversations_with_users(self, token):
        """ Функция для получения информации о беседах с пользователями """
        info_resp = requests.get(
            'https://api.vk.com/method/messages.getConversations',
            params={
                'access_token': token,
                'v': 5.131,

            }
        )
        return info_resp

    def creating_user_class(self, user_id):
        current_user = user_settings.User(self.user_token, user_id, self)
        current_user.set_options_from_profile()
        return current_user

    def checking_user_message(self, flag_request=False):
        """
        Проверка сообщения от пользователя
        :return:
        """
        active_users = {}
        while True:
            current_conversations_json = self.get_conversations_with_users(self.group_token).json()
            for i in range(current_conversations_json['response']['count']):
                if 'unread_count' in current_conversations_json['response']['items'][i]['conversation'].keys():
                    if current_conversations_json['response']['items'][i]['conversation']['unread_count'] >= 1:
                        user_message = current_conversations_json['response']['items'][i]['last_message']['text']
                        if str(user_message).lower() == 'начать':
                            user_id = current_conversations_json['response']['items'][i]['conversation']['peer']['id']
                            current_user = self.creating_user_class(user_id)
                            active_users[user_id] = current_user

            if len(active_users) > 0:
                print(active_users)
                return active_users

