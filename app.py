import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import warnings
import numpy as np
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Dashboard - Programas Internacionales",
                page_icon="🌎",
                layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title('🌎 Dashboard - Programas Internacionales')
df=pd.read_csv('https://raw.githubusercontent.com/totemunn/programas-internacionales/main/df_prog.csv')
df=df.replace('EUA','USA')

st.sidebar.header("🌎 Dashboard - Programas Internacionales")

st.sidebar.subheader('Filtros:')

with st.sidebar:
#    year_choice=df['int_year'].unique().tolist()
#    select_year=st.selectbox('Escoja el año:',year_choice)
    school_choice=df['school'].unique().tolist()
    select_school=st.selectbox('Escoja la escuela:',school_choice)
    first_choice=df['first_choice'].unique().tolist()
    select_choice=st.selectbox('¿Primera opción?:',first_choice)


st.markdown('##')

intercambio = (df['type'] == 'INT').sum()
no_int = (df['type'] != 'INT').sum() 
continent_total=df['continent'].value_counts().head(5)
country_total=df['country'].value_counts().head(5)
calificaciones=round(df['average'].mean(),2)

st.markdown('### KPIs')
st.write('Estos son algunos KPIs de Programas Internacionales.')
left_column,middle_column,right_column=st.columns(3)
left_column.metric('Alumnos que fueron de intercambio:',intercambio,'alumnos')
middle_column.metric('Alumnos que se fueron a otros programas:',no_int,'alumnos')
right_column.metric('Calificación promedio:',calificaciones)

st.markdown('##')
df_filt=df.loc[(df['first_choice']== select_choice) & (df['school'] == select_school),['int_year','school','first_choice']]
df_filt=df_filt.int_year.value_counts()
df_filt=pd.DataFrame(df_filt)
df_filt=df_filt.reset_index()
df_filt=df_filt.rename(columns={'index':'Year','int_year':'Cant_Alumnos'})
df_filt = df_filt.astype({'Year':'int'})
df_filt=df_filt.sort_values(by='Year')


st.markdown('---')
st.markdown('### Cantidad de alumnos que se fueron a su primera opción a través de los años')
st.write('Con los filtros en el sidebar puedes visualizar cuántos alumnos se fueron a su primera opción por escuela a través de los años.')
fig_line = px.line(df_filt, x='Year', y="Cant_Alumnos",markers=True)

fig_line['data'][0]['line']['color']='#F33A6A'
fig_line.update_xaxes(type='category')

st.plotly_chart(fig_line)

labels = ['1st choice','Otros']
values = [23885,1639]

with st.container():
    st.write("---")
    st.subheader('')
    st.write('##')
    st.markdown("<h1 style='text-align: center; color: #F33A6A; font-size: 25px;'>El porcentaje de alumnos que quedan en su primer opción</h1>", unsafe_allow_html=True)
    fig_opcion=px.pie(values=values,
    names=labels,color=labels,
    color_discrete_map={'1st choice':'#F33A6A','Otros':'#FFB6C1'},template='plotly_white',hole=.4) 
    fig_opcion.update_traces(textposition='outside',marker=dict(line=dict(color='#F33A6A',width=3)),rotation=80)
    st.plotly_chart(fig_opcion)

    st.markdown("<h1 style='text-align: center; color: #F33A6A; font-size: 18px;'>El 93.6% de los alumnos quedan en su primer opción; el resto de los alumnos quedan en otra.</h1>", unsafe_allow_html=True)

df_sank=pd.read_csv('https://raw.githubusercontent.com/totemunn/programas-internacionales/main/df_prog.csv')


df_sank = df[['school', 'type', 'continent']]
df_sank.school = df_sank.school.astype('category').cat.codes
df_sank.type = df_sank.type.astype('category').cat.codes
df_sank.continent = df_sank.continent.astype('category').cat.codes

num_escuela = list(df_sank.school.unique())
tipoescuela = list(df.school.unique())

num_type = list(df_sank.type.unique())
tipotype = list(df.type.unique())

num_continent = list(df_sank.continent.unique())
tipocontinent = list(df.continent.unique())

escuela_dim = go.parcats.Dimension(values = df_sank.school, label = 'Escuela', categoryarray = num_escuela, ticktext = tipoescuela)
tipo_dim = go.parcats.Dimension(values = df_sank.type, label = 'Tipo de intercambio', categoryarray = num_type, ticktext = tipotype)
continent_dim = go.parcats.Dimension(values = df_sank.continent, label = 'Continente', categoryarray = num_continent, ticktext = tipocontinent)

color = df_sank.school

fig5 = go.Figure(data = [go.Parcats(dimensions = [escuela_dim, tipo_dim, continent_dim],
        line={'color': color,'colorscale':'pinkyl'},
        labelfont={'size': 15, 'family': 'Arial', 'color': '#F33A6A'},
        tickfont={'size': 12, 'family': 'Arial', 'color': '#F33A6A'},
        arrangement='freeform')
        ])

colores = ['#000000', '#FFFFFF']
fuentes = ['Arial']

fig5.update_layout(paper_bgcolor = colores[1], #Color del background,
                  hoverlabel_font_family = fuentes[0], hoverlabel_font_size = 15,) #Formato de la descripción emergente

with st.container():
    st.write("---")
    left_column, right_column = st.columns([1, 4])
    with left_column:
        st.subheader('Diagrama de Sankey')
        st.write('##')
        st.write('Los estudiantes de Negocios e Ingeniería son los que más se internacionalizan.')
        st.write('La gran mayoría de los alumnos NO se van de intercambio, se van a otro tipo de programas.')
    with right_column:
        st.plotly_chart(fig5, use_container_width=True)

country_total=pd.DataFrame(country_total)
continent_total=pd.DataFrame(continent_total)

country_total.reset_index(inplace=True)
country_total=country_total.rename(columns={'index': 'Country','country':'No_Alumnos',})

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
st.markdown(hide_table_row_index, unsafe_allow_html=True)


df_map=df[['country','continent']]
df_map=df_map.country.value_counts()
df_map=pd.DataFrame(df_map)
df_map=df_map.reset_index()
df_map=df_map.rename(columns={'index':'country','country':'students'})

df3 = pd.read_csv('country-and-continent-codes-list.csv')
df3=df3.drop(['Continent_Code','Country_Name','Two_Letter_Country_Code','Country_Number'],axis=1)
df3['Three_Letter_Country_Code'] = df3['Three_Letter_Country_Code'].replace(['USA'], 'EUA')

df_map = df_map.merge(df3, how = 'inner', left_on = 'country', right_on = 'Three_Letter_Country_Code')
df_map = df_map.drop(['Three_Letter_Country_Code'],axis=1)
df_map.rename(columns = {'Continent_Name':'continent'}, inplace = True)

fig_mapa = px.scatter_geo(df_map, locations="country", color="continent",
                     hover_name="country", size="students",
                     projection="natural earth", color_continuous_scale='pinkyl')

with st.container():
    st.write("---")
    left_column, right_column = st.columns([1.5,2.5])
    with left_column:
        st.subheader('Top 5 Países')
        st.write('##')
        st.write('Los alumnos se van principalmente a países europeos.')
        st.write('Los países más populares son España, Canadá y Francia.')
        st.table(country_total)
    with right_column:
        st.plotly_chart(fig_mapa)


hide_st_style="""
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style
            """

st.markdown(hide_st_style,unsafe_allow_html=True)
