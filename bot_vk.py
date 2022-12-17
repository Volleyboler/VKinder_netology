import random
import requests

import private_token
import user_settings


class BotVK:
    def __init__(self):
        ...

    @staticmethod
    def write_msg(token, user_id, message='empty message', attachments=''):
        """Функция отправки сообщения пользователю"""

        info_resp = requests.get(
            'https://api.vk.com/method/messages.send',
            params={
                'random_id': random.randrange(10 ** 7),
                'access_token': token,
                'v': 5.131,
                'user_id': user_id,
                'message': message,
                'attachments': attachments,
                #                 'keyboard': {}
            }
        )
        return info_resp

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

    def checking_user_message(self, active_users: dict):
        while True:
            current_conversations_json = self.get_conversations_with_users(private_token.TOKEN_APP).json()
            for i in range(current_conversations_json['response']['count']):
                try:
                    if (current_conversations_json['response']['items'][i]['conversation']['unread_count'] >= 1 and
                            str(current_conversations_json['response']['items'][i]['last_message']['text']
                                ).lower() == 'начать'):
                        user_settings.User(private_token.TOKEN,
                                           current_conversations_json['response']['items'][i]['conversation']['peer'][
                                               'id'])
                        current_user = user_settings.User(private_token.TOKEN,
                                                          current_conversations_json['response']['items'][i][
                                                              'conversation']['peer']['id'])
                        current_user.set_options_from_profile()
                        active_users[current_conversations_json['response']['items'][i]['conversation'][
                            'peer']['id']] = current_user
                except:
                    continue
                finally:
                    ...
            if len(active_users) > 0:
                print(active_users)
                return active_users

    def checking_start_message(self):
        active_users = {}
        while True:
            current_conversations_json = self.get_conversations_with_users(private_token.TOKEN_APP).json()
            for i in range(current_conversations_json['response']['count']):
                try:
                    if (current_conversations_json['response']['items'][i]['conversation']['unread_count'] >= 1 and
                            str(current_conversations_json['response']['items'][i]['last_message']['text']
                                ).lower() == 'начать'):
                        user_settings.User(private_token.TOKEN,
                                           current_conversations_json['response']['items'][i]['conversation']['peer'][
                                               'id'])
                        current_user = user_settings.User(private_token.TOKEN,
                                                          current_conversations_json['response']['items'][i][
                                                              'conversation']['peer']['id'])
                        current_user.set_options_from_profile()
                        active_users[current_conversations_json['response']['items'][i]['conversation'][
                            'peer']['id']] = current_user
                except:
                    ...
                finally:
                    ...
            if len(active_users) > 0:
                print(active_users)
                return active_users

