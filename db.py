import asyncpg
from flask import Flask
from select import select
from peewee import PostgresqlDatabase

db = PostgresqlDatabase(user="postgres",
                        password="ruslan46576",
                        host="localhost",
                        port="5432",
                        database="busstation")

# Функция для установления подключения к базе данных
async def create_db_connection():
    return await asyncpg.connect(
        user='postgres',
        password='ruslan46576',
        host='localhost',
        port=5432,
        database='busstation'
    )


# Регистрация пользователя
async def cmd_start_db(user_id, user_name):
    # Установление подключения к базе данных
    connection = await create_db_connection()
    # Проверка существования пользователя в таблице
    user = await connection.fetchrow("SELECT * FROM users WHERE user_id = $1", user_id)
    if not user:
        # Вставка данных в таблицу с использованием параметризированного запроса
        await connection.execute("INSERT INTO users (user_id, name) VALUES ($1, $2)", user_id, user_name)

    # Закрытие подключения
    await connection.close()


# Добавление рейса в расписание
async def add_bus_in_schedule(bus_id, index):
    connection = await create_db_connection()

    date = await connection.fetchval("SELECT data FROM schedule WHERE id = $1", index)
    await connection.execute("INSERT INTO schedule (data, bus_id) VALUES ($1, $2)",
                             date, bus_id)

    await connection.close()


# Добавление нового автобуса
async def add_bus(state):
    async with state.proxy() as data:
        connection = await create_db_connection()
        await connection.execute(
            "INSERT INTO buses (coming, price) VALUES ($1, $2)",
            data['coming'], data['price']
        )
    await connection.close()


# Удаление автобуса и его рейсов
async def delete_bus(id):
    connection = await create_db_connection()
    # Удаляем автобус с таблицы buses
    await connection.execute("DELETE FROM buses WHERE id = $1", id)
    # Удаляем все рейсы автобуса с таблицы schedule
    await connection.execute("DELETE FROM schedule WHERE bus_id = $1", id)
    await connection.close()


# Возвращает ID если нашелся автобус с именем name
async def get_bus_id(name):
    try:
        # Установление подключения к базе данных
        connection = await create_db_connection()
        bus = await connection.fetchval("SELECT id FROM buses WHERE coming = $1", name)
        return bus
    finally:
        await connection.close()


# Возвращает name если нашелся автобус с таким ID
async def get_bus_name(id):
    try:
        # Установление подключения к базе данных
        connection = await create_db_connection()
        bus = await connection.fetchval("SELECT coming FROM buses WHERE id = $1", id)
        return bus
    finally:
        await connection.close()


# Извлечение истории покупок пользователя
async def get_by_history_user(user_id):
    connection = await create_db_connection()
    try:
        # Выполнение запроса к базе данных для извлечения покупок пользователя
        by_history = await connection.fetch(
            "SELECT bus_name, date_by, date_travel, place FROM history WHERE user_id = $1", user_id)
        return by_history
    finally:
        await connection.close()


# Извлечение истории покупок всех пользователей
async def get_by_history():
    connection = await create_db_connection()
    try:
        # Выполнение запроса к базе данных для извлечения покупок всех пользователей
        by_history = await connection.fetch("SELECT id, user_id, bus_name, date_by, date_travel, place FROM history")
        return by_history
    finally:
        await connection.close()


# Извлечение всех рейсов
async def get_buses():
    connection = await create_db_connection()
    try:
        # Выполнение запроса к базе данных для извлечения рейсов
        buses = await connection.fetch("SELECT * FROM buses")
        return buses
    finally:
        await connection.close()


# Извлечения ID, даты и количество свободных мест
async def get_data_and_place(bus_id):
    connection = await create_db_connection()
    try:
        # Выполнение запроса к базе данных для извлечения ID, даты и количество свободных мест
        places = await connection.fetch("SELECT id, data, places FROM schedule WHERE bus_id = $1 ORDER BY id ASC ",
                                        bus_id)
        return places
    finally:
        await connection.close()