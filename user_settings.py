import datetime

import requests

import bot_vk
import private_token
import dictionaries_vk


class User:

    def __init__(self, token, user_id):
        """
        Дата рождения,
        пол,
        город,
        семейное положение.
        """
        self.token = token
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

    def get_search_options(self):
        ...

    # def send_msg_to_adding_info(self, empty_info_list: list):
    #     requesting_info_string = ",".join(empty_info_list)
    #     print(f"Ошибка! В вашем профиле необходимо заполнить поля: {requesting_info_string}.")
    #     ...

    def set_options_from_profile(self):
        result_response = self.get_profile_info().json()
        empty_info_list = []
        print(result_response)
        try:
            self.first_name = result_response['response'][0]['first_name']
        except:
            print('Отсутствует имя пользователя')
        try:
            self.last_name = result_response['response'][0]['last_name']
        except:
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
        except:
            empty_info_list.append("год рождения")
        try:
            self.sex = result_response['response'][0]['sex']
        except:
            empty_info_list.append("пол")
        try:
            self.city = result_response['response'][0]['city']
        except:
            empty_info_list.append("город")
        try:
            self.relation = result_response['response'][0]['relation']
        except:
            empty_info_list.append("статус отношений")

        print(self.age)
        print(self.sex)
        print(self.city)
        print(self.relation)
        if len(empty_info_list) > 0:
            message_user_info = f"Для корректной работы поиска необходимо заполнить следующие поля в вашем профиле:\n {', '.join(empty_info_list)}."
        else:
            message_user_info = f"Информация вашего профиля:\nВозраст: {self.age}\nпол: {dictionaries_vk.sex_dict[self.sex]}\nгород: {self.city['title']}\nсемейное положение: {dictionaries_vk.relations_dict[self.sex][self.relation]}."
        print(message_user_info)
        # time.sleep(1.0)
        bot_vk.BotVK.write_msg(private_token.GROUP_TOKEN, self.id, message_user_info)
