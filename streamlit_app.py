#Создание СППР с помощью streamlit

import streamlit as st  #Streamlit — это фреймворк для языка программирования Python

from Start import start  #стартовая страница, пока не открылись вкладки задач

from Investment import investment  #задача "Оценка инвестиций"
from Consumption import consumption #задача "Потребление товаров"
from Credit import credit  #задача "Кредитные расчёты"
from Criteria import criteria  #задача "Выбор в условиях неопределённости и риска"
from Risk import risk  #задача "Оптимальное портфельное инвестирование"


#st.title("Моя СППР")  #главный заголовок сайта
#tabs = st.tabs(["Оценка инвестиций", "Потребление товаров", "Кредитные расчёты", "Выбор в условиях неопределённости и риска", "Оптимальное портфельное инвестирование"])  #вкладки сайта
#так как вкладки плохо прокручиваются, если их много, то было принято их разделить на два блока: Расчётные задачи и Экстремальные задачи 



with st.sidebar: #боковая панель с кнопками задач для отображения информации без загромождения основной области контента веб-приложений 
    start_page = st.button("Наша СППР", use_container_width = True, type = "primary")
    spravka = st.link_button("Справочные материалы", "https://drive.google.com/file/d/1axEnVY1CuVmp_QWRzVPQka1LkbQjONJA/view?usp=sharing", icon = '❓') #кнопка "Справочные материалы" с ссылкой на pdf-файл со справочными материалами по задачам
    
    tasks = st.radio(
        "Выберете финансово-экономическую задачу:",
        ("Оценка инвестиций",
         "Кредитные расчёты",
         "Выбор в условиях неопределённости и риска",
         "Потребление товаров",
         "Оптимальное портфельное инвестирование")
        )

if start_page:
    start()
else:
    if tasks == "Оценка инвестиций":
        investment()
    elif tasks == "Кредитные расчёты":
        credit()
    elif tasks == "Выбор в условиях неопределённости и риска":
        criteria()
    elif tasks == "Потребление товаров":
        consumption()
    elif tasks == "Оптимальное портфельное инвестирование":
        risk()
