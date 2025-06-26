# Телеграм-бот Быстрый Шеф
import sqlite3
import telebot
from telebot import types
from telebot.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup 
from telebot.types import WebAppInfo

bot = telebot.TeleBot('7390999869:AAHr4ggvhQZcpExaEtiuw9Ck2SWHjgCcMe8') # Айди нашего бота

autorizen_user = {} # Сохраняем состояние пользователя

# Таблицы БД
def init_db():
    connU = sqlite3.connect('users.db')
    curU = connU.cursor()
    
    # Таблица, хранящая в себе всю информацию о пользователе
    curU.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        items TEXT NOT NULL,  
        address TEXT NOT NULL,
        status TEXT DEFAULT 'pending'
        )""")
    connU.commit() # Сохраняем таблицу
    
    # Отключаем сеть
    curU.close()
    connU.close()
    
    connF = sqlite3.connect('menufoods.db')
    curF = connF.cursor()
    
    # Создаём таблицу, хранящую в себе меню блюд и всю информацию о них
    curF.execute("""CREATE TABLE IF NOT EXISTS menufoods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_dish TEXT NOT NULL,
        ingredients TEXT NOT NULL,
        cost_dish REAL NOT NULL,
        image_url TEXT
        )""")
    connF.commit() # Сохраняем таблицу
    
    # Отключаем сеть
    curF.close()
    connF.close()

init_db() # Включаем таблицы БД в программу

# Добавляем фунцию для добавления еды в таблицу БД
def add_dish(name_dish, ingredients, cost_dish, image_url=None):
    try:
        connF = sqlite3.connect('menufoods.db')
        curF = connF.cursor()
                                    
        # Указываем названия колонок и используем параметризованный запрос
        curF.execute("""
            INSERT OR IGNORE INTO menufoods 
            (name_dish, ingredients, cost_dish, image_url) 
            VALUES (?, ?, ?, ?)
        """, (name_dish, ingredients, cost_dish, image_url))
        
        connF.commit()
        curF.close()
        connF.close()

    except ValueError as e:
        print(f"Ошибка: {e}")
        curF.close()
        connF.close()
        
# Добавляем пиццу в таблицу БД для примера
add_dish("Пицца 4 сыра", "моцарелла, тильзитер, пармезан, дор блю, сливочный соус", 1000.0, 'images?q=tbn:ANd9GcSv_xjGfKRaEQWbo5B_bQRQhuTu8h9BNKZnNQ&s')

# Меню, главная страница
@bot.message_handler(commands=['start'])
def menu(message):
    # Создаём кнопки
    markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    make_order = types.KeyboardButton('Сделать заказ')
    my_order = types.KeyboardButton('Мои заказы')
    menu_dish = types.KeyboardButton('Меню')
    markup_menu.add(make_order, my_order, menu_dish)
    
    wellcome_message = """Вас приветствует заВилка!\n
Выберите действие для дальнейшего развития событий"""
    wellcome_photo = open('templatesimg/Bot-Telegram-Telegram-SHef-povar-min.jpg', 'rb')
    
    bot.send_message(message.chat.id, wellcome_message, reply_markup=markup_menu)
    bot.send_photo(message.chat.id, wellcome_photo)

# Данный декоратор открывает мини-приложение в Телеграме с меню
@bot.message_handler(func=lambda message: message.text == 'Меню')
def menu_info(message):
    menu_info = InlineKeyboardMarkup() # Добавляет возможность создать кнопку с WebAppInfo
    
    # Добавление кнопки, где WebAppInfo открывает хостинг нашего сайта в Telegram-боте
    menu_info.add(InlineKeyboardButton("Открыть меню заВилка", web_app=WebAppInfo(url="htttps://SHOKERRR777.github.io")))
    bot.send_message(message.chat.id, "Откройте меню, чтобы продолжить", reply_markup=menu_info)
    
bot.polling(none_stop=True) # Чтобы наш бот не прекращал работать