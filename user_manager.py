"""Содержит базовую реализацию менеджера пользователя при помощи паттерна Одиночка"""


class UserManagerUser:
    def __init__(self):
        self.__registration = None

    @property
    def registration(self):
        return self.__registration

    @registration.setter
    def registration(self, flag):
        self.__registration = flag
        return
