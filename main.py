from sqlalchemy import exc

import bot_vk
import private_token
import dictionaries_vk
import data_base_users as db

"""
Путь к токенам:
private_token.USER_TOKEN  - токен пользователя
private_token.GROUP_TOKEN - токен группы

Взаимодействие группы с пользователем в чате начинается после того как пользователь напишет в чате "Начать" 


current_users = {} ввел на будущее, чтобы попробовать библиотеку asyncio, сейчас скрипт в один момент времени работает 
только с одним пользователем
"""


def interaction_with_user(group_bot_vk, user, user_id):
    """
    Функция взаимодействия с пользователем
    :param group_bot_vk:
    :param user:
    :param user_id:
    :return:
    """
    while True:
        user_answer = group_bot_vk.get_info_from_user(user_id=user_id,
                                                      message=dictionaries_vk.options_messages['start'],
                                                      answers_list=['1', '2'])
        if user_answer == '1':
            group_bot_vk.searching_users(user_id, user)
        elif user_answer == '2':
            group_bot_vk.write_msg(user_id=user_id, message=dictionaries_vk.options_messages['end_work'])
            return False


def main():
    """
    Функция создает экземпляр бота
    :return:
    """
    current_users = {}
    group_bot_vk = bot_vk.BotVK(private_token.USER_TOKEN, private_token.GROUP_TOKEN)
    while True:
        writing_users = group_bot_vk.checking_user_message()
        for user_id in writing_users.keys():
            if user_id not in current_users.keys():
                current_users[user_id] = True
                user = writing_users[user_id]
                vk_user = db.VKUser(user_id, user.first_name, user.last_name, user.age, user.sex, user.city)
                session = db.Session()
                try:
                    session.add(vk_user)
                    session.commit()
                except exc.IntegrityError:
                    print('User already in BD')
                current_users[user_id] = interaction_with_user(group_bot_vk, user, user_id)


if __name__ == '__main__':
    main()
