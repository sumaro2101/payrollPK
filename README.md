# Данный проект предназначен для бухгалтерского учета.
Бухгалтер может создавать персонал и назначать ему логин, пароль и зарплату
Персонал может заходить и просматривать других пользователей кроме зарпалаты.
Пользователь может видеть только свою зарпалату, исключение администратор и Бухгалтер.

# Установка и пользование
## Для установки неоходимо в первую очередь иметь PostgreSQL
В ".env.sample" укажите неоходимые параметры (3 параметра базы данных) и переменуйте файл в ".env"
Создайте базы данных с такими названиями которые были указанны в ".env".
Должно быть 2 базы данных, тестовая и основная.

## Установите виртуальноe окружение и зависимости:
1. poetry init
2. poetry install
3. poetry shell
(Убедитесь что подключился нужный интерпретатор)

## Создайте папку
1. Создайте папку в backend с названием static

## Создайте сертификаты
1. Перейдите в папку certs
cd backend/certs
В README.md
Описана инструкция по созданию сертификатов

## Попробуйте запустить сервер:
1. uvicorn main:app
Если запуск прошел успешно можете продолжать.
Если у вас высвечивается warning каждый 2 секунды, проверьте запущен ли сервер СУБД.

## Установите миграции alembic:
1. alembic upgrade head

## Создайте администратора:
1. python backend/api_v1/users/superuser.py
(Логин и пароль вы указываете в ".env")

## Можно начинать
Можете зайти на http://localhost:8000/docs#/ и посмотреть все возможности проекта.
