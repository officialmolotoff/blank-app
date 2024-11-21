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
    st.title("Наша СППР")
    st.link_button("Справочные материалы", "https://drive.google.com/file/d/1axEnVY1CuVmp_QWRzVPQka1LkbQjONJA/view?usp=sharing", icon = '❓') #кнопка "Справочные материалы" с ссылкой на pdf-файл со справочными материалами по задачам
    investment_task = st.button("Оценка инвестиций", use_container_width = True)#установка use_container_width = True заставляет кнопку заполнять ширину своего контейнера
    credit_task = st.button("Кредитные расчёты", use_container_width = True)
    criteria_task = st.button("Выбор в условиях неопределённости и риска", use_container_width = True)
    consumption_task = st.button("Потребление товаров", use_container_width = True)
    risk_task = st.button("Оптимальное портфельное инвестирование", use_container_width = True)

#работа кнопок на боковой панели 
if investment_task:
    investment()
elif credit_task:
    credit()
elif criteria_task:
    criteria()
elif consumption_task:
    consumption()
elif risk_task:
    risk()
else:      #стартовая страница, пока не открылись вкладки задач
    start()



