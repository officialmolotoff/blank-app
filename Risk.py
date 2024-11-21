#вкладка "Оптимальное портфельное инвестирование"

import streamlit as st  #Streamlit — это фреймворк для языка программирования Python
import pandas as pd   #для вывода таблиц (в виде dataframe)
import numpy as np
from scipy.optimize import minimize, LinearConstraint  #для поиска минимума функции
import matplotlib.pyplot as plt  #для графика

def risk():  #tabs - это вкладки; number - номер данной вкладки, который передаётся из Main

    st.title("Оптимальное портфельное инвестирование")
    
    st.info("Задача представляет собой выбор структуры портфеля так, чтобы обеспечить заданное значение ожидаемой доходности, и при этом риск портфеля был бы минимальным")  #голубое поле с текстом

    #числовое поле ввода для количества видов ценных бумаг в портфеле
    n = st.number_input("Количество видов ценных бумаг в портфеле:",
                            min_value = 2,
                            value = 2,
                            step = 1)

    #числовое поле ввода для ожидаемой доходности портфеля
    m_p = st.number_input("Ожидаемая доходность портфеля:",
                            step = 0.01)

    #создание таблицы для возможности ввода пользователем ожидаемых доходностей ценных бумаг
    m = pd.DataFrame(
    {
        "Вид ценных бумаг": [i+1 for i in range (n)],
        "Ожидаемая доходность": [0.0 for i in range (n)],
    })
    m = st.data_editor(
        m, #вставка колонок из DataFrame m
        #конфигурация колонок
        column_config = {  
            "Ожидаемая доходность": st.column_config.NumberColumn(   
                step = 0.01,
                format = "%f руб.",
                required = True
            ),
            "Вид ценных бумаг": st.column_config.NumberColumn(  
                disabled = True
            )
        },
        hide_index = True
    )
    
    m_mas = m["Ожидаемая доходность"].tolist() #считывание введённых пользователем значений ожидаемых доходностей ценных бумаг в список

    #далее заполнениие пользователем матрицы ковариаций
    st.write(f"Заполните матрицу ковариаций:")

    a = {"Вид ценных бумаг": [i+1 for i in range (n)]}   
    b = {"Вид ценных бумаг": st.column_config.NumberColumn(  
        disabled = True
    )}
    for i in range(n):  
        a[f"{i+1}"] = [0.0 for j in range (n)]  
        b[f"{i+1}"] = st.column_config.NumberColumn(  
            step = 0.01,
            required = True
        )
    data_df = pd.DataFrame(a)
    data_df = st.data_editor(data_df, column_config = b, hide_index = True)

    V = data_df.drop("Вид ценных бумаг", axis = 1).to_numpy().tolist() #считывание введённых пользователем значений ковариаций ценных бумаг в матрицу

    if len(set(m_mas)) == 1 and m_mas[0] != m_p:  #проверка, что ограничения задачи Марковица (x_1 + x_2 + ... = 1 и m_1*x_1 + m_2*x_2 + ... = m_p) не являются противоречивыми
        st.error(f"При одинаковом значении доходностей для всех ценных бумаг значение ожидаемой доходности портфеля не может быть отлично от ожидаемой доходности любой из ценных бумаг.\n\
                           Пожалуйста, введите ожидаемую доходность портфеля, равную {m_mas[0]}")
    elif not(np.array_equal(V, np.array(V).transpose())):  #проверка, что матрица V является симметричной
        st.error(f"Введённая матрица не симметрична")
    elif not(np.all(np.linalg.eigvals(V) > 0)):  #проверка, что матрица V является положительно определённой
        st.error(f"Введённая матрица не положительно определена")
    else: #если все условия проверены, то решается задача Марковица
        # D_p = x^T*V*x -> min
        # x_1 + x_2 + ... + x_n = 1
        # m_1*x_1 + m_2*x_2 + ... + m_n*x_n = m_p
        def f(x):  #необходимо "собрать" функцию, которую будем минимизировать, аргументом которой будет только структура портфеля x
            summa = 0
            for i in range (n):
                for j in range (n):
                    summa += V[i][j]*x[i]*x[j]
            return summa
        #далее код для создания линейных ограничений в виде объекта LinearConstraint
        #B             A             C
        #1 <= x_1 + x_2 + ... x_n <= 1
        #m_p <= m_1*x_1 + m_2*x_2 + ... + m_n*x_n <= m_p
        #матрица A представляет собой "центральную" матрицу для создания ограничений в виде объекта LinearConstraint
        A = [[1 for i in range (n)]] #в первой строчке матрицы A будут коэффы при x-сах в ограничении: x_1 + x_2 + ... x_n (то есть это единицы)
        A.append(m_mas)   #во второй строчке матрицы A будут коэффы при x-сах в ограничении:  m_1*x_1 + m_2*x_2 + ... + m_n*x_n (то есть это вектор m_mas)
        B = [1, m_p] #матрица B представляет собой "левую" матрицу для создания оганичений в виде объекта LinearConstraint 
        C = [1, m_p]  #матрица C представляет собой "правую" матрицу для создания оганичений в виде объекта LinearConstraint
        linear_constraint = LinearConstraint(A, B, C)
        x_start = np.array([0 for i in range(n)]) #x_start представляет собой начальное предположение точки минимума
        result = minimize(f, x_start, method = 'trust-constr', constraints = linear_constraint)
        x = result.x.tolist() #запись значений вектора x = (x_1, x_2, ...)
        min_f = f(x) #нахождение значения дисперсии (квадрата риска) для этой структуры портфеля

        #вывод результата
        s = 'Структура портфеля с наименьшим риском: ('
        for i in x:
            s += f'{round(i,3)}, '
        s = s[0:-2]  #срез от нулевого элемента строки до (-2), чтобы убрать запятую и пробел после последнего элемента
        s += ')'
        st.write(s)
        st.write(f"Его риск: {min_f**(1/2)}")

        #далее код для построения графика фронта Марковица по принципу получения значений точек (ожидаемая доходность портфеля, риск портфеля)
        if len(set(m_mas)) != 1:  #график не имеет смысла, если все значения ожидаемых доходностей ценных бумаг равны между собой, так как тогда возможно только единтсвенное значение m_p
            #график будет строиться путём нахождения значений риска для значений ожидаемых доходностей портфеля
            m_h = m_p/10  #шаг между ожидаемыми доходностями будет m_p/10
            mas_m_p_h = [0] #первая ожидаемая доходность будет равна 0
            for i in range(20): #будет найдено 20 значений риска для ожидаемых доходностей портфеля
                mas_m_p_h.append(mas_m_p_h[i] + m_h)
            res_mas = []
            for i in mas_m_p_h:
                A = [[1 for i in range (n)]] 
                A.append(m_mas)   
                B = [1, i] 
                C = [1, i]  
                linear_constraint = LinearConstraint(A, B, C)
                x_start = np.array([0 for i in range(n)]) 
                result = minimize(f, x_start, method = 'trust-constr', constraints = linear_constraint)
                x = result.x.tolist() 
                min_f = f(x) 
                res_mas.append(min_f**0.5)

            a = pd.DataFrame(
            {
                "Ожидаемые доходности портфеля": mas_m_p_h,
                "Минимальный риск портфеля": res_mas
            })
            fig, ax1 = plt.subplots()
            ax1.plot(a["Ожидаемые доходности портфеля"], a["Минимальный риск портфеля"], '-')
            ax1.plot(a["Ожидаемые доходности портфеля"][10], a["Минимальный риск портфеля"][10], '-o')
            #ax1.vlines(n_0, -K, K, linestyles='dashed', colors='red')
            #ax1.axvline(m_p, color='red', linestyle='dashed')
            ax1.axvline(0, color='black')
            ax1.axhline(0, color='black')
            ax1.legend(['Фронт Марковица', 'Решение задачи'])
            ax1.grid()
            ax1.set_xlabel('Ожидаемые доходности портфеля')
            ax1.set_ylabel('Минимальный риск портфеля')
            st.pyplot(fig)
        else:
            fig, ax1 = plt.subplots()
            ax1.plot(m_p, min_f**0.5, '-o')
            ax1.axvline(0, color='black')
            ax1.axhline(0, color='black')
            ax1.legend(['Решение задачи'])
            ax1.grid()
            ax1.set_xlabel('Ожидаемые доходности портфеля')
            ax1.set_ylabel('Минимальный риск портфеля')
            st.pyplot(fig)
        






