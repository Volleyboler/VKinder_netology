import requests

import private_token
import user_settings
import comparing_results
import data_base_users

# self.token = token
#         self.birth_date = ''
#         self.sex = 0
#         self.city = {}
#         self.relation = 0


def get_search_results(token, age_from, age_to, sex, city_id, status):
    """ Функция для получения информации искомого пользователя """
    info_resp = requests.get(
        'https://api.vk.com/method/users.search',
        params={
            'access_token': token,
            'v': 5.131,
            'city_id': city_id,
            'sex': sex,
            'age_from': age_from,
            'age_to': age_to,
            'status': status,
        }
    )
    return info_resp
