import sqlite3 as sql
from datetime import datetime


def connect_database() -> sql.Connection:
    """
    Создает подключение к таблице 'users' в БД.
    Если не найдена таблица или БД - функция создает их.
    :return: Возвращает экземпляр класса Connection, через который осуществляется работа с БД
    """

    connect = sql.connect('database.db')
    data = connect.execute("select count(*) from sqlite_master where type='table' and name='users'")
    for row in data:
        if row[0] == 0:
            with connect:
                connect.execute("""
                CREATE TABLE users (
                tg_id INTEGER,
                schedule VARCHAR(50)
                );
                """)
    return connect


class User:
    """
    Класс для работы с записями о пользователях в БД
    Для инициализации объекта необходим ID пользователя в Telegram типа INT

    Доступные методы:
    add_to_db();
    change_schedule();
    """

    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    def add_to_db(self) -> None:
        """
        Добавляет новую запись о пользователе в БД
        """

        db_connect = connect_database()
        query = 'INSERT INTO users (tg_id) values (?)'
        with db_connect:
            db_connect.execute(query, (self.tg_id, ))

    def change_schedule(self, schedule_time: str) -> str:
        """
        Изменяет расписание отправки сообщения для пользователя
        Проверяется значение аргументы schedule_time на соответствие формату
        :param schedule_time: часы и минуты в формате строки HH:MM
        :return: Возвращает сообщение о результате работы функции
        """

        try:
            schedule_time = datetime.strptime(schedule_time, '%H:%M').strftime('%H:%M')
        except ValueError:
            return 'Время должно быть указано в формате HH:MM'

        db_connect = connect_database()
        query = 'UPDATE users SET schedule=? WHERE tg_id=?'
        with db_connect:
            db_connect.execute(query, (schedule_time, self.tg_id))
        return 'Расписание установлено'
