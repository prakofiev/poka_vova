import pandas as pd
import numpy as np
import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode, GridOptionsBuilder, JsCode
from PIL import Image
from streamlit_echarts import st_echarts
import datetime as dt


st.set_page_config(page_title="Пока с Вовой", layout="wide")

data = pd.read_csv('data.csv')
data = data[pd.to_datetime(data['Дата']) <= dt.datetime.today()][:4]

data['total'] = data.iloc[:, 1:].sum(axis=1)
data.columns = [col.strip() for col in data.columns]


results = data.iloc[:, 1:-1].sum().sort_values(ascending=False).reset_index()

results.columns = ['Игрок', 'Баллы']
results['Место'] = list(range(1, len(results)+1))
results = results.sort_values(by='Место')
results = results[['Место', 'Игрок', 'Баллы']]



st.title('Пока с Вовой')

players = {
    'Дашулик': ('dashulik.jpeg', 'Меня зовут Даша, я давно интересуюсь играми, но серьёзного опыта пока не имею:) В свободное время экспериментирую на кухне и увлекаюсь танцами. '),
    'Маша': ('masha.jpeg', 'Люблю настолки, рисовать и пешие прогулки :)'),
    'Таня': ('tanya.jpeg', 'В свободное время люблю играть в волейбол.'),
    'Даша П.': ('dashap.jpeg', 'Помимо прочего люблю кино, танцы, играть  на муз. инструментах, приятные компании.'),
    'Настя': ('nastya.jpeg', 'В свободное от работы время убиваю монстров в Тристраме, гуляю с собакой, участвую в квизах. Люблю путешествовать по разным странам и любоваться архитектурой.'),
    'Юля': ('julia.jpeg', 'В свободное время люблю смотреть сериальчики и читать.'),
    'Женя': ('zhenya.jpeg', 'Помимо компьютерных игр, увлекаюсь ирландскими танцами.'),
    'Денис': ('denis.jpeg', 'Я получил педагогическое и психологическое образование. Успел набраться опыта в этих сферах, работая с детьми и взрослыми в разных проектах. Помимо компьютерных игр, интересуюсь волейболом, фридайвингом и этим летом хотел бы попробовать себя в фехтование и поиграть в D&D')
}

cols = st.columns(2, gap='large')

with cols[0]:
    
    st.header('Турнирная таблица')
    gb = GridOptionsBuilder.from_dataframe(results)
    gb.configure_column("Место", width='15%')
    gb.configure_column("Игрок", width='70%')
    gb.configure_column("Баллы", width='15%')
    gridoptions = gb.build()

    AgGrid(
        results, 
        gridOptions=gridoptions, 
        key='links_table', 
        reload_data=True,
        update_mode=GridUpdateMode.GRID_CHANGED, 
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=True, 
        enable_enterprise_modules=False,
    )
    
    option = {
        'title': {'text': 'Статистика прощаний по дням'},
        'xAxis': {
            'type': 'category',
            'data': list(data['Дата']),
            'axisTick': {
                'alignWithLabel': True
            }
        },
        'yAxis': {
            'type': 'value',
            'name': 'Кол-во прощаний'
        },
        'series': [
            {
            'data': list(data['total']),
            'type': 'bar',
            'label': {'show': True}
            }
        ]
    }; 
    
    st_echarts(
        options=option
    )

with cols[1]:
    st.header('Статистика по игрокам')
    
    selected_player = st.selectbox(
        label='Выберите игрока',
        options=players.keys()
    )
    
    image = Image.open(f'photos/{players[selected_player][0]}')

    player_cols = st.columns([1,3], gap='small')

    with player_cols[0]:
        st.image(image, width=150)
        
    with player_cols[1]:
        st.subheader('Об игроке')
        st.write(players[selected_player][1])
        
    cols = st.columns([1,3])    
    
    with cols[0]:
        st.metric(label="Рейтинг прощаний", value=f'{int(data[selected_player].sum() / len(data) * 100)} %')
    with cols[1]:
    
        options = {
            'grid': {'top': 0, 'right': 0, 'left': 0},
            'xAxis': {
                'type': 'category',
                'data': data['Дата'].to_list(),
                'splitArea': {
                    'show': True
                }
            },
            'yAxis': {
                'type': 'category',
                'show': False,
                'data': [selected_player],
                'splitArea': {
                    'show': True
                }
            },
            'series': [
                {
                'name': 'Punch Card',
                'type': 'heatmap',
                'data': [
                        {
                            'value': [date, selected_player, val * 1],
                            'itemStyle': {
                                'color': '#5470c6' if val else '#F2F8FD'
                            }
                        } for date, val in zip(data['Дата'].to_list(), data[selected_player].to_list())
                    ],
                'label': {
                    'show': False
                }
                }
            ]
        }
        
        st_echarts(
            options=options,
            height=130
        )
        
st.write("Реклама моего [инстаграма](https://instagram.com/prakofiev)")