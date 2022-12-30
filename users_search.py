import requests


class UsersSearch:
    def __init__(self, user_token: str, user_id: int, age: int, sex: int, city: dict, relation: int):
        self.token = user_token
        self.age = age
        self.sex = sex
        self.city = city
        self.relation = relation
        self.user_id = user_id

    def get_search_results(self, offset=0):
        """
        Метод формирует запрос на поиск пользователей, основываясь на параметрах профиля пользователя инициирующего поиск
        :param offset: сдвиг выборки
        :return: объект результат запроса
        """
        params = self._calculating_search_parameters()
        print(params)
        info_resp = requests.get(
            'https://api.vk.com/method/users.search',
            params={
                'access_token': self.token,
                'v': 5.131,
                'city_id': params['city_id'],
                'sex': params['sex'],
                'age_from': params['age_from'],
                'age_to': params['age_to'],
                'status': params['status'],
                'count': 1000,
                'offset': offset,
                'fields': 'domain, bdate, city, sex'
            }
        )
        return info_resp

    def _calculating_search_parameters(self):
        """
        Вычисление данных поиска на основе информации пользователя
        :return:
        """
        if self.age == 18:
            age_from = 18
        else:
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
        """
        Метод возвращает 3 фотографии пользователя исходя из количества лайков и комментариев
        :param photos_info: результат запроса всех фото профиля пользователя в формате json
        :return: список с описанием 3 фото
        """
        best_photos = []
        for photo in photos_info['response']['items']:
            name_photo = f"photo{photo['owner_id']}_{photo['id']}"
            count_likes_and_comments = photo['likes']['count'] + photo['comments']['count']
            best_photos.append((count_likes_and_comments, name_photo))
        if len(best_photos) > 2:
            best_photos.sort(reverse=True)
            return [best_photos[0][1], best_photos[1][1], best_photos[2][1]]
        else:
            return False

    # def searching_users(self):
    #     """
    #
    #     :return:
    #     """
    #     param_offset = 0
    #     count = 1
    #     while param_offset < count:
    #         search_results = self.get_search_results(offset=param_offset,).json()
    #         print(search_results)
    #         count = search_results['response']['count']
    #         param_offset += 1000
    #         data_base_users.data_base_of_good_results[self.user_id] = []
    #         for user_number in search_results['response']['items']:
    #             time.sleep(0.2)
    #             photos_info = self.get_user_photos(user_number['id']).json()
    #             if 'response' in photos_info.keys():
    #                 photos = self.get_best_photos(photos_info)
    #                 if photos:
    #                     message_about_profile = f"{user_number['first_name']} {user_number['last_name']}\nhttps://vk" \
    #                                             f".com/{user_number['domain']} "
    #                     self.bot_instance.write_msg(self.user_id, message=message_about_profile,
    #                                                 attachment=",".join(photos))
    #
    #                     data_base_users.data_base_of_good_results[self.user_id].append({user_number['id']: photos})

    def get_user_photos(self, owner_id):
        """
        Метод получения всех фото профиля пользователя
        :param owner_id: id пользователя, по которому запрашивается информация
        :return: объект ответа на запрос
        """
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




