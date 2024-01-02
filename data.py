# TODO: Добавить базу


def save_new_user(user_id=0, user_name=None):
    print(user_id, user_name)
    # TODO: Добавить юхера в базу


def find_user(user_name):
    # TODO: Найти и вернуть юзера в базе
    return None


def add_to_list(to_user_id, add_user_name):
    add_user_id = find_user(add_user_name)
    if add_user_id == None:
        return "Данный пользователь ещё не использует этого бота. Отправьте ему ссылку"

    # TODO: Добавить друга в список

    return f"{add_user_name} добавлен в ваш список"


def del_from_list(to_user_id, del_user_name):
    del_user_id = find_user(del_user_name)
    if del_user_id == None:
        return "Данный пользователь не найден в вашем списке"

    # TODO: Удалить друга из списка

    return f"{del_user_id} удален из вашего списка"


def get_users_list(user_id=0) -> list:
    # TODO: Взять список друзей юзера из базы
    pass


def timer_for_checking():
    # TODO: Сделать проверку, кто не отписался, что ок, и разослать его списку
    pass
