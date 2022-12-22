import requests
import time

import bot_vk
import data_base_users

# self.token = token
#         self.birth_date = ''
#         self.sex = 0
#         self.city = {}
#         self.relation = 0

class UsersSearch:
    def __init__(self, token: str, user_id: int, age: int, sex: int, city: dict, relation: int):
        self.token = token
        self.age = age
        self.sex = sex
        self.city = city
        self.relation = relation
        self.user_id = user_id

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
        age_from = self.age - 1
        age_to = self.age + 1
        if self.sex == 1:
            sex = 2
        elif self.sex == 2:
            sex = 1
        else:
            sex = self.sex
        city_id = self.city['id']
        status = self.relation
        return {'age_from': age_from, 'age_to': age_to, 'sex': sex, 'city_id': city_id, 'status': status}

    def get_best_photos(self, photos_info):
        best_photos = {}
        for photo in photos_info['response']['items']:
            name_photo = f"<photo><{photo['owner_id']}><{photo['id']}>"
            best_photos[name_photo] = photo['likes']['count'] + photo['comments']['count']
            time.sleep(0.5)
        best_photos_sorted = dict(sorted(best_photos.items(), key=(lambda item: item[1])))
        return best_photos_sorted.keys[-1:-4]

    def searching_users(self):
        params = self.calculating_search_parameters()
        # bot_vk.BotVK.write_msg()
        param_offset = 0
        counts = 1
        while param_offset < counts:
            search_results = self.get_search_results(self.token, params['age_from'], params['age_to'], params['sex'], params['city_id'], params['status'], offset=0,).json()
            # print(search_results)
            counts = search_results['response']['count']
            param_offset += 1000
            data_base_users.data_base_of_results[self.user_id] = []
            for user_number in search_results['response']['items']:
                # print(user_number)
                try:
                    photos_info = self.get_user_photos(user_number['id'])
                    print(photos_info.json())
                    photos = self.get_best_photos(photos_info.json())
                    print(photos)
                except:
                    continue
                data_base_users.data_base_of_results[self.user_id].append({user_number['id']: photos})

    def get_user_photos(self, owner_id):
        """ Получаем информацию о фотографиях профиля искомого пользователя """

        info_resp = requests.get(
            'https://api.vk.com/method/photos.get',
            params={
                'access_token': self.token,
                'v': 5.131,
                'album_id': 'profile',
                'extended': 1,
                'owner_id': owner_id,
            }
        )
        return info_resp




