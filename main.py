# from random import randrange
#
# import vk
# from vk.longpoll import VkLongPoll, VkEventType
#
# token = input('Token: ')
#
# vk.session.search()
#
# vk = vk.VkApi(token=token)
# longpoll = VkLongPoll(vk)
#
#
#
# def write_msg(user_id, message):
#     vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})
#
#
# for event in longpoll.listen():
#     if event.type == VkEventType.MESSAGE_NEW:
#
#         if event.to_me:
#             request = event.text
#
#             if request == "привет":
#                 write_msg(event.user_id, f"Хай, {event.user_id}")
#             elif request == "пока":
#                 write_msg(event.user_id, "Пока((")
#             else:
#                 write_msg(event.user_id, "Не поняла вашего ответа...")


import requests

import private_token
import user_settings
import users_search
import comparing_results
import data_base_users


def making_info_response(token):
    """ Функция для получения информации искомого пользователя """
    info_resp = requests.get(
        'https://api.vk.com/method/users.search',
        params={
            'access_token': token,
            'v': 5.131,

        }
    )
    return info_resp


y = user_settings.SearchUsersOptions(private_token.TOKEN)

x = making_info_response(private_token.TOKEN)

print(y.city)
print(y.sex)
print(y.birth_day)
print(y.relation)


y.set_options_from_profile()
print(y.city)
print(y.sex)
print(y.birth_day)
print(y.relation)


print(x.json())

