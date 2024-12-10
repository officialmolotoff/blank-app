#вкладка "Выбор в условиях неопределённости и риска"

import streamlit as st  #Streamlit — это фреймворк для языка программирования Python
import pandas as pd  #для создания таблиц (в виде dataframe)
import numpy as np  #для возможности быстрого (через функцию) нахождения максимума по столбцу 

def criteria():  #tabs - это вкладки; number - номер данной вкладки, который передаётся из Main

    st.title("Выбор в условиях неопределённости и риска")

    st.info("Задача представляет собой расчёт критериев принятия решений в условиях неопределённости и риска") #голубое поле с текстом

    #числовое поле ввода для количества вариантов решения
    n = st.number_input("Количество вариантов решения:",
                                min_value = 2,
                                value = 2,
                                step = 1)

    #числовое поле ввода для количества внешних условий
    m = st.number_input("Количество внешних условий:",
                                min_value = 2,
                                value = 2,
                                step = 1)

    #создание таблицы для возможности ввода пользователем значений внешних условий в виде матрицы n*m
    a = {"Вариант решения": [i+1 for i in range (n)]}   #значения для первого столбца "Вариант решения" 
    b = {"Вариант решения": st.column_config.NumberColumn(  #конфигурация для первого столбца "Вариант решения", которая не позволяет менять значения
                            disabled = True
                        )}
    for i in range(m):  #создание m столбцов "Значение внешнего условия 1, 2, 3, ..." и их конфигураций
        a[f"Значение внешнего условия {i+1}"] = [0.0 for j in range (n)]  #значения по умолчанию для столбцов "Значение внешнего условия 1, 2, 3, ..."
        b[f"Значение внешнего условия {i+1}"] = st.column_config.NumberColumn(  #конфигурация для столбцов "Значение внешнего условия 1, 2, 3, ..."
                            required = True
                        )
    data_df = pd.DataFrame(a)
    data_df = st.data_editor(data_df, column_config = b, hide_index = True)

    sets = data_df.drop("Вариант решения", axis = 1).to_numpy().tolist() #сбор введённых пользователем значений внешних условий в матрицу, где i - номер варианта решения, j - значение внешнего условия j

    #выбор: известно ли распределение вероятностей для внешних условий или нет
    options = ["Да", "Нет"]
    ok = st.radio("Известно ли распределение вероятностей для внешних условий?", options)

    #если известно распределение вероятностей для внешних условий
    if ok == "Да":
        #создание таблицы для возможности ввода вероятностей для внешних условий
        prob = pd.DataFrame(
            {
                "Внешние условия": [i+1 for i in range (m)],
                "Вероятности": [0.01 for i in range (m)],
            }
        )
        prob = st.data_editor(
            prob,
            column_config = {
                "Вероятности": st.column_config.NumberColumn(
                    min_value = 0.01,
                    step = 0.01,
                    format = "%f",
                    required = True
                ),
                "Внешние условия": st.column_config.NumberColumn(
                    disabled = True
                )
            },
            hide_index = True
        )

        probs_mas = prob["Вероятности"].tolist() #считывание введённых пользователем значений вероятностей в список

        if sum(probs_mas) != 1:  #проверка, что вероятности в сумме дают 1
            st.error(f"Введённые вероятности при внешних условиях должны в сумме давать 1. Текущая сумма: {sum(probs_mas)}")
        else:
            #подсчёт минимаксного критерия
            crit_mm = [min(sets[i]) for i in range(n)] #ищется минимальное значение в каждой строке
            max_crit_mm = max(crit_mm) #среди всех минимальных ищется максимальное

            #подсчёт критерия Сэвиджа
            np_sets = np.array(sets)  #преобразование матрицы в np.array для возможности поиска максимума в столбцах
            max_colomn = np.amax(np_sets, axis = 0).tolist()  #создание списка максимумов по столбцам матрицы sets
            crit_s = [max([max_colomn[j] - sets[i][j] for j in range(m)]) for i in range(n)] #создание матрицы путём вычитания из максимума по столбцам элементов этого столбца; нахождение максимума по строкам
            min_crit_s = min(crit_s) #нахождение минимума из максимумов 

            #подсчёт критерия Байеса-Лапласа
            sets_p = [ [sets[i][j] * probs_mas[j] for j in range(m)] for i in range(n)]  #создание матрицы путём перемножения элементов на соответствующие вероятности
            crit_bl_p = [sum(sets_p[i]) for i in range(n)]  #создание списка путём сложения элементов строк 
            max_crit_bl_p = max(crit_bl_p)  #нахождение максимума из этого списка
            
            #будет идти подсчёт количества "побед" вариантов решения по критериям (для вывода наилучших вариантов)
            wins = [0 for i in range(n)]  #изначально "побед" у каждого варианта 0
            sets_mm = []  #"победы" по минимаксному критерию
            sets_s = []   #"победы" по критерию Сэвиджа
            sets_bl = []  #"победы" по критерию Байеса-Лапласа
            for i in range(n):  #пробегаем по всем вариантам решения
                if crit_mm[i] == max_crit_mm: #если вариант имеет максимальное значение по минимаксному критерию
                    wins[i] += 1  #плюс одна победа идёт этому варианту
                    sets_mm.append('+')  #добавляется плюсик в sets_mm для вывода столбца минимаксного критерия по всем вариантам решения
                else:  #если не максимальное значение по минимаксному критерию
                    sets_mm.append('-')  #добавляется минус в sets_mm для вывода столбца минимаксного критерия по всем вариантам решения
                #аналогично для критериев Сэвиджа и Байеса-Лапласа
                if crit_s[i] == min_crit_s:
                    wins[i] += 1
                    sets_s.append('+')
                else:
                    sets_s.append('-')
                if crit_bl_p[i] == max_crit_bl_p:
                    wins[i] += 1
                    sets_bl.append('+')
                else:
                    sets_bl.append('-')

            #вывод результата в виде таблицы
            #            Минимаксный     Сэвидж    Байес-Лаплас
            #     1         +/-            +/-         +/-
            #     2         +/-            +/-         +/-
            #    ...        ...            ...         ...
            #     m         +/-            +/-         +/-
            result = pd.DataFrame(
                {
                    "Варианты решений": [i+1 for i in range (n)],
                    "Минимаксный критерий": sets_mm,
                    "Критерий Севиджа": sets_s,
                    "Критерий Байесса-Лапласа": sets_bl,
                }
            )
            result = st.data_editor(
                result.style.applymap(lambda x: 'background-color : #a0ff9b' if x == "+" else 'background-color : #ff6c6c' if x == "-" else ''),  #"+" - зелёная ячейка; "-" - красная
                column_config = {
                    "Минимаксный критерий": st.column_config.TextColumn(
                        disabled = True
                    ),
                    "Критерий Севиджа": st.column_config.TextColumn(
                        disabled = True
                    ),
                    "Критерий Байесса-Лапласа": st.column_config.TextColumn(
                        disabled = True
                    ),
                    "Варианты решений": st.column_config.NumberColumn(
                        disabled = True
                    )
                },
                hide_index = True
            )

            #дальнейший код для вывода номеров наилучших вариантов решений
            max_wins = max(wins)
            string = ''
            for i in range(len(wins)):
                if wins[i] == max_wins:
                    string += str(i+1) + ', '
            st.write(f"Наилучшие варианты решений: {string[:-2]}")

    else:  #если неизвестно распределение вероятностей для внешних условий
        #всё аналогично, но без вычисления критерия Байеса-Лапласа

        crit_mm = [min(sets[i]) for i in range(n)]
        max_crit_mm = max(crit_mm)

        np_sets = np.array(sets)
        max_colomn = np.amax(np_sets,axis = 0).tolist()
        crit_s = [max([max_colomn[j] - sets[i][j] for j in range(m)]) for i in range(n)]
        min_crit_s = min(crit_s)

        wins = [0 for i in range(n)]
        sets_mm = []
        sets_s = []
        for i in range(n):
            if crit_mm[i] == max_crit_mm:
                wins[i] += 1
                sets_mm.append('+')
            else:
                sets_mm.append('-')
            if crit_s[i] == min_crit_s:
                wins[i] += 1
                sets_s.append('+')
            else:
                sets_s.append('-')

        result = pd.DataFrame(
            {
                "Варианты решений": [i+1 for i in range (n)],
                "Минимаксный критерий": sets_mm,
                "Критерий Севиджа": sets_s
            }
        )
        result = st.data_editor(
            result.style.applymap(lambda x: 'background-color : #a0ff9b' if x == "+" else 'background-color : #ff6c6c' if x == "-" else ''),
            column_config = {
                "Минимаксный критерий": st.column_config.TextColumn(
                    disabled = True
                ),
                "Критерий Севиджа": st.column_config.TextColumn(
                    disabled = True
                ),
                "Варианты решений": st.column_config.NumberColumn(
                    disabled = True
                )
            },
            hide_index = True
        )

        max_wins = max(wins)
        string = ''
        for i in range(len(wins)):
            if wins[i] == max_wins:
                string += str(i+1) + ', '
        st.write(f"Наилучшие варианты решений: {string[:-2]}")
