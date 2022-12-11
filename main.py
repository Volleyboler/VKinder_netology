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
import random

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


def write_msg(token, user_id, message='empty message', attachments=''):
#     vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})
    info_resp = requests.get(
    'https://api.vk.com/method/messages.send',
    params={
        'random_id': random.randrange(10 ** 7),
        'access_token': token,
        'v': 5.131,
        'user_id': user_id,
        'message': message,
        'attachments': attachments,
        'group_id': 17668361
     }
    )
    return info_resp

# messages.allowMessagesFromGroup



y = user_settings.SearchUsersOptions(private_token.TOKEN)

x = making_info_response(private_token.TOKEN)

print(y.city)
print(y.sex)
print(y.birth_date)
print(y.relation)


y.set_options_from_profile()
print(y.city)
print(y.sex)
print(y.birth_date)
print(y.relation)
print(y.id)

print(x.json())

birth_year = y.birth_date.split('.')[2]
age_from = 2022 - int(birth_year) - 2
print(f'age_from = {age_from}')
age_to = 2022 - int(birth_year) + 2
print(f'age_to = {age_to}')


write_msg(private_token.TOKEN_APP, y.id)

print(users_search.get_search_results(private_token.TOKEN, age_from, age_to, 1, 1, y.relation).json())
# y.city['id']





