from sqlalchemy import exc
import sqlalchemy as sa

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


def get_dating_users(user_id):
    """
    Функция получает список избранных профилей для выбранного пользователя
    :param user_id:
    :return:
    """
    session = db.Session()
    query = session.query(db.DatingUser).filter(sa.or_(
        db.DatingUser.user_id == user_id)).all()
    return query


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
                                                      answers_list=['1', '2', '3'])
        if user_answer == '1':
            group_bot_vk.searching_users(user_id, user)
        elif user_answer == '2':
            query = get_dating_users(user_id)
            group_bot_vk.write_msg(user_id=user_id, message=f"Число записей в избранном: {len(query)}")
            for dating_profile in query:
                message_about_profile = f"{dating_profile.dating_user_first_name} " \
                                        f"{dating_profile.dating_user_last_name}\n{dating_profile.birthdate}" \
                                        f"\n{dating_profile.city}\nhttps://vk.com/{dating_profile.user_domain}"
                attachments_photo = dating_profile.best_photos
                group_bot_vk.write_msg(user_id=user_id, message=message_about_profile, attachment=attachments_photo)
        elif user_answer == '3':
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
                session.add(vk_user)
                try:
                    session.commit()
                except exc.IntegrityError:
                    print('User already in BD')
                current_users[user_id] = interaction_with_user(group_bot_vk, user, user_id)


if __name__ == '__main__':
    main()
