# импортируем библиотеку streamlit
import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

# Константы
DATA = 'data/jobs_in_data_2024.csv'


def show_salary(df: pd.DataFrame,
                factor: str,
                category: str) -> None:
    df['salary_in_usd'] = df['salary_in_usd']/1000
    # Посмотрим распределение ежемесячных расходов
    fig = plt.figure(figsize=(10, 6))
    plt.title(f'Распределение доходов в зависимости от {factor}. \n {category}')
    plt.grid(color='grey', linestyle='--')
    plt.xlabel('Заработная плата, тыс USD')

    # Определим диапазон для оси x
    x_min = round(0.90 * df.loc[df[factor] == category, 'salary_in_usd'].min() / 5) * 5
    x_max = round((1.1 * df.loc[df[factor] == category, 'salary_in_usd'].max()) / 10) * 10
    if (x_max - x_min) / 0.100 < 30:
        x_step = 0.1
    elif (x_max - x_min) / 0.200 < 30:
        x_step = 0.2
    elif (x_max - x_min) / 0.500 < 30:
        x_step = 0.500
    elif (x_max - x_min) / 1 < 30:
        x_step = 1
    elif (x_max - x_min) / 5 < 30:
        x_step = 5
    elif (x_max - x_min) / 10 < 30:
        x_step = 10
    elif (x_max - x_min) / 50 < 30:
        x_step = 50
    else:
        x_step = 100
    plt.xticks(np.arange(x_min, x_max + 1, x_step))
    plt.ylabel('Количество объектов')
    plt.hist(df.loc[df[factor] == category, 'salary_in_usd'],
             bins=np.arange(x_min, x_max, x_step))
    plt.show()
    st.pyplot(fig)


df = pd.read_csv(DATA)
st.title('Данные о зарплате в области анализа данных (2024 год)')

st.subheader('Распределение доходов в зависимости от различных факторов')

factor = st.sidebar.radio('Укажите исследуемый фактор: ',
                          ('experience_level', 'employment_type', 'job_category'))

category = 'other'
if factor:
    category = st.sidebar.selectbox(
        'Для каких категорий вывести распределение?', list(df[factor].unique()))
else:
    st.write('Выберите фактор')

show_salary(df, factor, category)
# display dataframe
st.dataframe(df)
