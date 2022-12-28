import requests
import random
import datetime

import bot_vk
import private_token
import users_search
import data_base_users


group_bot_vk = bot_vk.BotVK(private_token.USER_TOKEN, private_token.GROUP_TOKEN)
current_users = group_bot_vk.checking_user_message()
for user_id in current_users.keys():
    user = current_users[user_id]
    new_users_search = users_search.UsersSearch(private_token.USER_TOKEN, user_id, user.age, user.sex,
                                                user.city, user.relation, group_bot_vk)
    new_users_search.searching_users()
print(data_base_users.data_base_of_good_results)
print(len(data_base_users.data_base_of_good_results[17668361]))
