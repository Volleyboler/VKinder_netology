import requests
import random
import datetime

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
    """Функция отправки сообщения пользователю"""

    info_resp = requests.get(
        'https://api.vk.com/method/messages.send',
        params={
            'random_id': random.randrange(10 ** 7),
            'access_token': token,
            'v': 5.131,
            'user_id': user_id,
            'message': message,
            'attachments': attachments,
        }
    )
    return info_resp


# x = making_info_response(private_token.TOKEN)

# print(y.city)
# print(y.sex)
# print(y.birth_date)
# print(y.relation)
#
# y.set_options_from_profile()
# print(y.city)
# print(y.sex)
# print(y.birth_date)
# print(y.relation)
# print(y.id)

# print(x.json())
#
# birth_year = y.birth_date.split('.')[2]
# age_from = 2022 - int(birth_year) - 2
# print(f'age_from = {age_from}')
# age_to = 2022 - int(birth_year) + 2
# print(f'age_to = {age_to}')


def get_conversations_with_users(token):
    """ Функция для получения информации о беседах с пользователями """
    info_resp = requests.get(
        'https://api.vk.com/method/messages.getConversations',
        params={
            'access_token': token,
            'v': 5.131,

        }
    )
    return info_resp


def checking_start_message():
    active_users = {}
    while True:
        current_conversations_json = get_conversations_with_users(private_token.TOKEN_APP).json()
        for i in range(current_conversations_json['response']['count']):
            try:
                if (current_conversations_json['response']['items'][i]['conversation']['unread_count'] >= 1 and
                        str(current_conversations_json['response']['items'][i]['last_message']['text']
                            ).lower() == 'начать'):
                #    write_msg(private_token.TOKEN_APP,
                 #             current_conversations_json['response']['items'][i]['conversation']['peer']['id'],
                  #            current_conversations_json['response']['items'][i]['conversation']['peer']['id'])
                    print("check1")
                    print(private_token.TOKEN_APP)
                    print(current_conversations_json['response']['items'][i]['conversation']['peer']['id'])
                    user_settings.User(private_token.TOKEN_APP, current_conversations_json['response']['items'][i]['conversation']['peer']['id'])
                    print("checkUser")
                    current_user = user_settings.User(private_token.TOKEN_APP, current_conversations_json['response']['items'][i]['conversation']['peer']['id'])
                    print("check2")
                    current_user.set_options_from_profile()
                    print("check3")
                    active_users[current_conversations_json['response']['items'][i]['conversation'][
                        'peer']['id']] = current_user
                # print("check1")
                # print(active_users)

            except:
                ...
            finally:
                ...
        if len(active_users) > 0:
            print(active_users)
            return active_users

current_users = checking_start_message()

# for user_id, user in current_users.values():



# print(current_conversations_json['response']['items'][i]['conversation']['peer']['unread_count'])

# write_msg(private_token.TOKEN_APP, y.id)

# print(users_search.get_search_results(private_token.TOKEN, age_from, age_to, 1, 1, y.relation).json())
# y.city['id']

# print(int(datetime.time))
