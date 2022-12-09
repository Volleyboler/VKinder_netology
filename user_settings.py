import requests


class SearchUsersOptions:

    def __init__(self, token):
        """
        Дата рождения,
        пол,
        город,
        семейное положение.
        """
        self.token = token
        self.birth_date = ''
        self.sex = 0
        self.city = {}
        self.relation = 0
        self.id = 0

    def get_profile_info(self):
        """ Функция для получения информации искомого пользователя """
        info_resp = requests.get(
            'https://api.vk.com/method/account.getProfileInfo',
            params={
                'access_token': self.token,
                'v': 5.131,
            }
        )
        return info_resp

    def get_search_options(self):
        ...

    def check_profile_info(self):
        empty_info_list = []
        if self.birth_date == '':
            empty_info_list.append("дата рождения")
        if self.sex == 0:
            empty_info_list.append("пол")
        if self.city == {}:
            empty_info_list.append("город")
        if self.relation == 0:
            empty_info_list.append("статус отношений")
        return empty_info_list

    def send_msg_to_adding_info(self, empty_info_list: list):
        requesting_info_string = ",".join(empty_info_list)
        print(f"Ошибка! В вашем профиле необходимо заполнить поля: {requesting_info_string}.")
        ...

    def set_options_from_profile(self):
        result_response = self.get_profile_info()
        self.birth_date = result_response.json()['response']['bdate']
        self.sex = result_response.json()['response']['sex']
        self.city = result_response.json()['response']['city']
        self.relation = result_response.json()['response']['relation']
        self.id = result_response.json()['response']['id']
        empty_info_list = self.check_profile_info()
        if len(empty_info_list) > 0:
            self.send_msg_to_adding_info(empty_info_list)


