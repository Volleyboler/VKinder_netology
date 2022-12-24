import requests
import random
import datetime

import bot_vk
import private_token
import user_settings
import users_search
import comparing_results
import data_base_users


group_bot_vk = bot_vk.BotVK(private_token.USER_TOKEN, private_token.GROUP_TOKEN)
current_users = group_bot_vk.checking_start_message()
for user_id in current_users.keys():
    user = current_users[user_id]
    new_users_search = users_search.UsersSearch(private_token.USER_TOKEN, user_id, user.age, user.sex,
                                                user.city, user.relation)
    new_users_search.searching_users()
print(data_base_users.data_base_of_good_results)
print(len(data_base_users.data_base_of_good_results[17668361]))
# users_search.UsersSearch(current_users)
#
# print(data_base_users.data_base_of_results)


# user = user_settings.User(private_token.TOKEN_APP, 17668361)
# info = user.get_profile_info().json()
# print(info)




# for user_id, user in current_users.values():


# print(current_conversations_json['response']['items'][i]['conversation']['peer']['unread_count'])

# write_msg(private_token.TOKEN_APP, y.id)

# print(users_search.get_search_results(private_token.TOKEN, age_from, age_to, 1, 1, y.relation).json())
# y.city['id']

# print(int(datetime.time))
