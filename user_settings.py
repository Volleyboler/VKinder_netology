import requests


class SearchUsersOptions:

    def __init__(self, token):
        """
        Возраст,
        пол,
        город,
        семейное положение.
        """
        self.token = token
        self.birth_day = ''
        self.sex = 0
        self.city = {}
        self.relation = 0

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

    def set_options_from_profile(self):
        result_response = self.get_profile_info()
        self.birth_day = result_response.json()['response']['bdate']
        self.sex = result_response.json()['response']['sex']
        self.city = result_response.json()['response']['city']
        self.relation = result_response.json()['response']['relation']
