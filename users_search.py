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

class UsersSearch:
    def __init__(self, token: str, age: int, sex: int, city: dict, relation: int):
        self.token = token
        self.age = age
        self.sex = sex
        self.city = city
        self.relation = relation

    def get_search_results(self, token, age_from, age_to, sex, city_id, status, offset=0,):
        """  """

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
                'count': 1000,
                'offset': offset,
            }
        )
        return info_resp



    def calculating_search_parameters(self):


        return {'age_from': age_from, 'age_to': age_to, 'sex': sex, 'city_id': city_id, 'status': status}


    def searching_users(self):
        params = self.calculating_search_parameters()


        for i in ...:
            data_base_users.data_base_of_results[id].append[id]