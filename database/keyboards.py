from aiogram.types import ReplyKeyboardMarkup

main = ReplyKeyboardMarkup(resize_keyboard=True)
(main.add('Рейсы').
 add('История покупок')
 .add('Контакты'))

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
(main_admin.add('Рейсы')
 .add('История покупок')
 .add('Контакты').add('Панель администратора'))

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
(admin_panel.add('Добавить рейс')
 .add('Удалить рейс')
 .add('История покупок всех пользователей')
 .add('Сделать выгрузку данных')
 .add('В главное меню'))
