import random
import requests
import time
from sqlalchemy import exc

import dictionaries_vk
import user_settings
import users_search
import data_base_users as db


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

    def asking_question_get_answer_from_user(self, user_id=False, message='empty message',
                                             q_message='empty question message', attachment='', answers_list=[]):
        self.write_msg(user_id, message=message, attachment=attachment)
        while True:
            self.write_msg(user_id, message=q_message)
            user_answer = self.checking_user_message(user_id=user_id)
            if user_answer in answers_list:
                return user_answer
            self.write_msg(user_id, message='Неверная команда')

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
        current_user = user_settings.User(self.user_token, user_id)
        message_user_info, empty_info_list = current_user.set_options_from_profile()
        if len(empty_info_list) > 0:
            for parameter in empty_info_list:
                while True:
                    user_answer = self.asking_question_get_answer_from_user(user_id=user_id, message=message_user_info)

                    if parameter == 1:
                        ...
                    elif parameter == 2:
                        ...
                    elif parameter == 3:
                        ...
                    elif parameter == 4:
                        ...
        return current_user

    def searching_users(self, user_id, user_instance):
        """
        Метод поиска пары и добавления вариантов в БД
        :param user_id:
        :param user_instance:
        :return:
        """
        new_users_search = users_search.UsersSearch(self.user_token, user_id, user_instance.age, user_instance.sex,
                                                    user_instance.city, user_instance.relation)
        param_offset = 0
        count = 1
        session = db.Session()
        while param_offset < count:
            search_results = new_users_search.get_search_results(offset=param_offset, ).json()
            print(search_results)
            count = search_results['response']['count']
            param_offset += 1000
            for user_number in search_results['response']['items']:
                time.sleep(0.2)
                photos_info = new_users_search.get_user_photos(user_number['id']).json()
                if 'response' in photos_info.keys():
                    photos = new_users_search.get_best_photos(photos_info)
                    if photos:
                        message_about_profile = f"{user_number['first_name']} {user_number['last_name']}\n{user_number['bdate']}\n{user_number['city']['title']}\nhttps://vk.com/{user_number['domain']}"
                        # ПРОВЕРИТЬ НАЛИЧИЕ ПОЛЬЗОВАТЕЛЯ В БД
                        user_answer = self.asking_question_get_answer_from_user(user_id=user_id, message=message_about_profile, q_message=dictionaries_vk.options_messages['check_search'], attachment=",".join(photos), answers_list=['1', '2', '3', '4'])
                        if user_answer == '1':
                            dating_user = db.DatingUser(user_number['id'], user_number['first_name'],
                                                        user_number['last_name'], user_number['bdate'],
                                                        user_number['sex'], user_number['city'], user_number['domain'],
                                                        user_id)
                            try:
                                session.add(dating_user)
                                session.commit()
                            except exc.IntegrityError:
                                print('User already in BD')
                            print('пользователь добавлен в избранное')
                        elif user_answer == '2':
                            black_list_item = db.BlackList(user_number['id'], user_number['first_name'],
                                                        user_number['last_name'], user_number['bdate'],
                                                        user_number['sex'], user_number['city'], user_number['domain'],
                                                        user_id)
                            try:
                                session.add(black_list_item)
                                session.commit()
                            except exc.IntegrityError:
                                print('User already in BD')
                            print('пользователь добавлен в чс')
                        elif user_answer == '3':
                            continue
                        elif user_answer == '4':
                            return False
        return True

    def checking_user_message(self, user_id=False):
        """
        Проверка сообщения от пользователя
        :return:
        """
        if not user_id:
            active_users = {}
            while True:
                current_conversations_json = self.get_conversations_with_users(self.group_token).json()
                for i in range(current_conversations_json['response']['count']):
                    if 'unread_count' in current_conversations_json['response']['items'][i]['conversation'].keys():
                        if current_conversations_json['response']['items'][i]['conversation']['unread_count'] >= 1:
                            user_message = current_conversations_json['response']['items'][i]['last_message']['text']
                            if str(user_message).lower() == 'начать':
                                user_id = current_conversations_json['response']['items'][i]['conversation']['peer'][
                                    'id']
                                current_user = self.creating_user_class(user_id)
                                active_users[user_id] = current_user

                if len(active_users) > 0:
                    print(active_users)
                    return active_users
        else:
            while True:
                current_conversations_json = self.get_conversations_with_users(self.group_token).json()
                for i in range(current_conversations_json['response']['count']):
                    if current_conversations_json['response']['items'][i]['conversation']['peer']['id'] == user_id:
                        if 'unread_count' in current_conversations_json['response']['items'][i]['conversation'].keys():
                            if current_conversations_json['response']['items'][i]['conversation']['unread_count'] >= 1:
                                user_message = current_conversations_json['response']['items'][i]['last_message'][
                                    'text']
                                return str(user_message).lower()
                    else:
                        continue
