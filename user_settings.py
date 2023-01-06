import datetime
import requests

import dictionaries_vk


class User:

    def __init__(self, user_token, user_id):
        self.token = user_token
        self.age = ''
        self.sex = -1
        self.city = {}
        self.relation = -1
        self.id = user_id
        self.first_name = ''
        self.last_name = ''

    def get_profile_info(self):
        """ Функция для получения информации искомого пользователя """
        info_resp = requests.get(
            'https://api.vk.com/method/users.get',
            params={
                'user_ids': self.id,
                'access_token': self.token,
                'v': 5.131,
                'fields': 'relation, sex, bdate, city,'
            }
        )
        return info_resp

    def set_options_from_profile(self):
        result_response = self.get_profile_info().json()
        empty_info_list = []
        try:
            self.first_name = result_response['response'][0]['first_name']
        except KeyError:
            print('Отсутствует имя пользователя')
        try:
            self.last_name = result_response['response'][0]['last_name']
        except KeyError:
            print('Отсутствует фамилия пользователя')
        try:
            birth_date = result_response['response'][0]['bdate']
            birth_date_list = [int(x) for x in birth_date.split('.')]
            if len(birth_date_list) < 3:
                raise
            else:
                current_date_list = [int(x) for x in str(datetime.date.today()).split('-')]
                if current_date_list[1:2] >= birth_date_list[-2:-3]:
                    self.age = current_date_list[0] - birth_date_list[-1]
            if self.age < 18:
                raise ValueError
        except ValueError:
            empty_info_list.append("год рождения(Для использования сервиса необходим возраст 18+)")
        except KeyError:
            empty_info_list.append(1)
        try:
            self.sex = result_response['response'][0]['sex']
        except KeyError:
            empty_info_list.append(2)
        try:
            self.city = result_response['response'][0]['city']
        except KeyError:
            empty_info_list.append(3)
        try:
            self.relation = result_response['response'][0]['relation']
        except KeyError:
            empty_info_list.append(4)
        empty_info_string_list = [dictionaries_vk.parameters_dict[x] for x in empty_info_list]
        if len(empty_info_list) > 0:
            message_user_info = f"Для корректной работы поиска необходимо заполнить следующие поля в вашем профиле:\n {', '.join(empty_info_string_list)}.\n"
        else:
            message_user_info = f"Информация вашего профиля:\nВозраст: {self.age}\nпол: {dictionaries_vk.sex_dict[self.sex]}\nгород: {self.city['title']}\nсемейное положение: {dictionaries_vk.relations_dict[self.sex][self.relation]}."
        return message_user_info, empty_info_list
