# Flask, который соединяет телеграм-бота с html-файлом
from flask import Flask, render_template, request

app = Flask(__name__)

# Главное меню
@app.route('menu/<name>')
def menu_interface(name):
    try: 
        import sqlite3
        
        connF = sqlite3.connect('menufoods.db')
        curF = connF.cursor()
        
        curF.execute("SELECT * FROM menufoods")
        menu = curF.fetchall()
        
        menu_list = [] # Словарь, в котором будет храниться вся информация о еде
        for items in menu:
            menu_list.append({
             'id' : items[0],
             'name_dish' : items[1],
             'ingredients' : items[2],
             'cost_dish' : items[3],
             'image_url' : items[4]   
            })
                
        curF.close() # Закрываем сеть
        connF.close()
    
    # Обработчик ошибок
    except IOError as e:
        return f"Произошла ошибка: {e}!"
    except Exception as e:
        return f"Произошла ошибка Exceptions: {e}!"
    
    # Возвращаем HTML-файл в виде ответа на запрос пользователя
    return render_template('menu_interface.html', name=name, menu_list=menu_list)

# Запуск программы
if __name__ == "__main__":
    app.run(debug=True)