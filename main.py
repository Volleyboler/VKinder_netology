from sqlalchemy import exc

import bot_vk
import private_token
import dictionaries_vk
import data_base_users as db

"""
Путь к токенам:
private_token.USER_TOKEN  - токен пользователя
private_token.GROUP_TOKEN - токен группы
"""


def main():
    group_bot_vk = bot_vk.BotVK(private_token.USER_TOKEN, private_token.GROUP_TOKEN)
    while True:
        current_users = group_bot_vk.checking_user_message()
        for user_id in current_users.keys():
            user = current_users[user_id]
            vk_user = db.VKUser(user_id, user.first_name, user.last_name, user.age, user.sex, user.city)
            session = db.Session()
            try:
                session.add(vk_user)
                session.commit()
            except exc.IntegrityError:
                print('User already in BD')
            while True:
                user_answer = group_bot_vk.get_info_from_user(user_id=user_id,
                                                              message=dictionaries_vk.options_messages['start'],
                                                              answers_list=['1', '2'])
                if user_answer == '1':
                    group_bot_vk.searching_users(user_id, user)
                elif user_answer == '2':
                    group_bot_vk.write_msg(user_id=user_id, message=dictionaries_vk.options_messages['end_work'])
                    break


if __name__ == '__main__':
    main()
