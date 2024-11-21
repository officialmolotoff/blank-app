#вкладка "Кредитные расчёты"

import streamlit as st  #Streamlit — это фреймворк для языка программирования Python
import pandas as pd  #для создания таблиц (в виде dataframe)

def credit():  #tabs - это вкладки; number - номер данной вкладки, который передаётся из Main

    st.title("Кредитные расчёты")

    st.info("Задача представляет собой расчёт кредитных выплат клиента и вывод соответствующей схемы кредитования") #голубое поле с текстом

    #поле выбора для типа периода кредитования
    n_type = st.selectbox(
        "Выберите тип периода кредитования",
        ("Дни", "Месяцы", "Годы")
        )

    #числовое поле ввода для продолжительности кредитования
    n = st.number_input("Продолжительность кредитования:",
                                min_value = 1,
                                value = 1,
                                step = 1)

    #числовое поле ввода для размера кредита
    D = st.number_input("Размер кредита (в рублях):",
                                min_value = 0.01,
                                value = 0.01,
                                step = 0.01)

    #числовое поле ввода для годовой процентной ставки
    r = st.number_input("Годовая процентная ставка (в процентах):",
                                min_value = 0.01,
                                value = 0.01,
                                step = 0.01)

    #преобразование годовой процентной ставки
    if n_type == "Дни":
        r = r / (100 * 365)
    elif n_type == "Месяцы":
        r = r / (100 * 12)
    else:
        r = r / 100
        
    #выбор схемы погашения кредита
    options = ["Схема погашения кредита одним платежом в конце срока",
               "Схема погашения кредита дифференцированными платежами",
               "Схема погашения кредита аннуитетными платежами"]
    schema = st.radio("Выберите схему погашения кредита", options)

    #если выбрана схема погашения кредита одним платежом в конце срока
    if schema == "Схема погашения кредита одним платежом в конце срока":

        # Периоды   Остаток долга  Выплаты по долгу
        #    0             D               0
        #    1           D(1+r)            0
        #    2           D(1+r)^2          0
        #   ...            ...            ...
        #    n              0              S

        #S = D(1+r)^n

        #далее сбор значений в соответствующие массивы
        periods = [0]
        ost = [D]
        pay = [0]

        for i in range(n-1):
            periods.append(i+1)
            ost.append(ost[i]*(1+r))
            pay.append(0)

        periods.append(n)
        ost.append(0)
        pay.append(ost[n-1]*(1+r))

        #далее вывод таблицы схемы (в виде dataframe) 
        table = pd.DataFrame(
        {
            "Периоды": periods,
            "Остаток долга": ost,
            "Выплаты по долгу": pay
        } )
        table = st.data_editor(
            table, #вставка колонок из датафрейма table 
            #конфигурация колонок
            column_config = {  
                "Остаток долга": st.column_config.NumberColumn(   
                    step = 0.01,
                    format = "%.2f руб.",
                    disabled = True
                ),
                "Выплаты по долгу": st.column_config.NumberColumn(   
                    step = 0.01,
                    format = "%.2f руб.",
                    disabled = True
                ), 
                "Периоды": st.column_config.NumberColumn(  
                    disabled = True
                )
            },
            hide_index = True
        )

        #вывод переплаты по кредиту
        st.write(f"Переплата по кредиту: {round(pay[n]-D, 2)} руб.")

    if schema == "Схема погашения кредита дифференцированными платежами":

        #d_t = d = D/n, t = 1, ..., n.
        #%_t = D_(t−1)*r, t = 1, ..., n.
        #D_t = D_(t−1) − d, t = 1, ..., n.
        #y_t = d_t + %_t, t = 1, ..., n.

        # Периоды, t  Остаток долга, D_t  Погасительная выплата, d_t  Проценты, %_t      Выплаты по долгу, y_t
        #    0             D                           0                     0                     0
        #    1            D - d                        d                     Dr                  d + Dr
        #    2           D - 2d                        d                  (D - d)r            d + (D - d)r  
        #   ...            ...                        ...                    ...                   ...
        #    n              0                          d                (D - (n-1)d)r         d + (D - (n-1)d)r 

        #Переплата: y_1 + y_2 + ... + y_n − D

        #далее сбор значений в соответствующие массивы
        d = D/n
        periods = [0]
        ost = [D]
        pay_ost=[0]
        procent=[0]
        pay = [0]

        for i in range(n):
            periods.append(i+1)
            ost.append(D-(i+1)*d)
            pay_ost.append(d)
            procent.append(ost[i]*r)
            pay.append(pay_ost[i+1]+procent[i+1])

        
        #далее вывод таблицы схемы (в виде dataframe) 
        table = pd.DataFrame(
        {
            "Периоды": periods,
            "Остаток долга": ost,
            "Погасительная выплата": pay_ost,
            "Проценты": procent,
            "Выплаты по долгу": pay
        } )
        table = st.data_editor(
            table, #вставка колонок из датафрейма table 
            #конфигурация колонок
            column_config = {  
                "Остаток долга": st.column_config.NumberColumn(   
                    step = 0.01,
                    format = "%.2f руб.",
                    disabled = True
                ),
                "Выплаты по долгу": st.column_config.NumberColumn(   
                    step = 0.01,
                    format = "%.2f руб.",
                    disabled = True
                ),
                "Погасительная выплата": st.column_config.NumberColumn(   
                    step = 0.01,
                    format = "%.2f руб.",
                    disabled = True
                ),
                "Проценты": st.column_config.NumberColumn(   
                    step = 0.01,
                    format = "%.2f руб.",
                    disabled = True
                ), 
                "Периоды": st.column_config.NumberColumn(  
                    disabled = True
                )
            },
            hide_index = True
        )

        #вывод переплаты по кредиту
        st.write(f"Переплата по кредиту: {round(sum(pay)-D, 2)} руб.")

    if schema == "Схема погашения кредита аннуитетными платежами":

        #Фиксированная общая выплата y высчитывается по формуле: y = D*r*(1 + r)^n / ( (1 + r)^n − 1 ) 
        
        #d_t = y − %_t, t = 1, ..., n.
        #%_t = D_(t−1)r, t = 1, ..., n.
        #D_t = D_(t−1) − d_t, t = 1, ..., n.
        #y_t = y, t = 1, ..., n.

        # Периоды, t  Остаток долга, D_t    Погасительная выплата, d_t         Проценты, %_t         Выплаты по долгу, y_t
        #    0           D_0 = D                       0                          0                          0
        #    1          D_0 - d_1                 y - D_0*r                      D_0*r                       y
        #    2          D_1 - d_2               y - (D_0 - d_1)*r             (D_0 - d_1)*r                  y
        #   ...            ...                        ...                          ...                      ...
        #    n              0                   y - (D_(n-1) - d_(n-1))*r   (D_(n-1) - d_(n-1))*r            y

        #Переплата: y * n − D

        #далее сбор значений в соответствующие массивы
        y = (D*r*(1+r)**n)/((1+r)**n-1)
        
        periods = [0]
        ost = [D]
        pay_ost=[0]
        procent=[0]
        pay = [0]

        for i in range(n):
            periods.append(i+1)
            procent.append(ost[i]*r)
            pay.append(y)
            pay_ost.append(pay[i+1]-procent[i+1])
            ost.append(ost[i]-pay_ost[i+1])

        
        #далее вывод таблицы схемы (в виде dataframe) 
        table = pd.DataFrame(
        {
            "Периоды": periods,
            "Остаток долга": ost,
            "Погасительная выплата": pay_ost,
            "Проценты": procent,
            "Выплаты по долгу": pay
        } )
        table = st.data_editor(
            table, #вставка колонок из датафрейма table 
            #конфигурация колонок
            column_config = {  
                "Остаток долга": st.column_config.NumberColumn(   
                    step = 0.01,
                    format = "%.2f руб.",
                    disabled = True
                ),
                "Выплаты по долгу": st.column_config.NumberColumn(   
                    step = 0.01,
                    format = "%.2f руб.",
                    disabled = True
                ),
                "Погасительная выплата": st.column_config.NumberColumn(   
                    step = 0.01,
                    format = "%.2f руб.",
                    disabled = True
                ),
                "Проценты": st.column_config.NumberColumn(   
                    step = 0.01,
                    format = "%.2f руб.",
                    disabled = True
                ), 
                "Периоды": st.column_config.NumberColumn(  
                    disabled = True
                )
            },
            hide_index = True
        )

        #вывод переплаты по кредиту
        st.write(f"Переплата по кредиту: {round(sum(pay)-D, 2)} руб.")
        
    
