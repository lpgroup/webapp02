# myFirstStreamlitApp.py
#import the libraries
import streamlit as st
from PIL import Image
from io import BytesIO
import requests
import pandas as pd
import plotly.graph_objects as go

import altair as alt
from urllib.error import URLError

r = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vR0IgfLCiAnnWqcgQTx1xz96FcSFUMDEHD-aWHT2DA-5Lfh9QfZYZbcYwqAhrVKRSrV3D7moFA8Hqka/pub?gid=980421081&single=true&output=csv')
data = r.content
df = pd.read_csv(BytesIO(data), index_col=0)
df.columns = ['email', 'Nome', 'NotaMiniCursos', 'NotaOrganizacao', 'Sugestao']
nREGISTROS = len(df)
df1 = df['NotaMiniCursos'].value_counts()
nPromotores = float(df1[9]) + float(df1[10])
PorcentagemPromotoes = nPromotores/nREGISTROS
# Count frequency value using GroupBy.size()
df1 = df.groupby(['NotaMiniCursos']).size()
nDetratores = 0
PorcentagemDetratores = nDetratores/nREGISTROS
nPromotores = float(df1[9]) + float(df1[10])
PorcentagemPromotoes = nPromotores/nREGISTROS
NPS = (PorcentagemPromotoes - PorcentagemDetratores)*100


image01 = Image.open('desenvolvimento.jpg')
# Use st.title("") para adicionar um TÍTULO ao seu Web app
st.title("Tecnologia de Informação e Comunicação - TIC (6ºT)")
# Use st.header("") para adicionar um CABEÇALHO ao seu Web app
# st.header("Cabeçalho")
# Use st.subheader("") para adicionar um SUB CABEÇALHO ao seu Web app
#st.subheader("Sub Cabeçalho")
# Use st.write("") para adicionar um texto ao seu Web app
#st.write("Como já deve ter percebido, o método st.write() é usado para escrita de texto e informações gerais!")
st.subheader("------ **Desenvolvido por: Massaki de O. Igarashi** -----")

menu = ["NPS_MackRede_13abr22",
        "Análise de Dados",
        # "Texto_Colunas",
        # "Texto_Markdown",
        # "Inserir_Figura"
        ]
choice = st.sidebar.selectbox("Menu de Opções",menu)
st.sidebar.write("Texto Side Bar")

if choice == "NPS_MackRede_13abr22": 
    st.header("Avaliações do Evento MackRede 13/abr/22")
    st.markdown(
    """
    - Se -100 < NPS <=  0: Zona Crítica
    - Se    0 < NPS <= 50: Zona de Aperfeiçoamento
    - Se   50 < NPS <= 75: Zona de Qualidade
    - Se   75 < NPS <=100: Zona de Excelência
    """)
    st.header("NPS = ")  
    st.subheader(NPS) 
    if (-100 < NPS and NPS <=  0): 
        st.warning("Zona Crítica")
    if (0 < NPS and NPS <= 50): 
        st.info("Zona de Aperfeiçoamento")
    if (50 < NPS and NPS <= 75):
        st.info("Zona de Qualidade")
    if (75 < NPS and NPS<=100): 
        st.info("Zona de Excelência")    
elif choice == "Análise de Dados": 
    #st.set_page_config(page_title="DataFrame Demo", page_icon="📊")

    st.markdown("# DataFrame Demo")
    st.sidebar.header("DataFrame Demo")
    st.write(
        """This demo shows how to use `st.write` to visualize Pandas DataFrames.
    (Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
    )


    @st.cache
    def get_UN_data():
        AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
        df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
        return df.set_index("Region")


    try:
        df = get_UN_data()
        countries = st.multiselect(
            "Choose countries", list(df.index), ["China", "United States of America"]
        )
        if not countries:
            st.error("Please select at least one country.")
        else:
            data = df.loc[countries]
            data /= 1000000.0
            st.write("### Gross Agricultural Production ($B)", data.sort_index())

            data = data.T.reset_index()
            data = pd.melt(data, id_vars=["index"]).rename(
                columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
            )
            chart = (
                alt.Chart(data)
                .mark_area(opacity=0.3)
                .encode(
                    x="year:T",
                    y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                    color="Region:N",
                )
            )
            st.altair_chart(chart, use_container_width=True)
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
        """
            % e.reason
        )
elif choice == "Texto_Colunas":       
    st.subheader("Texto formatado em colunas")
    st.write("Veja a seguir uma opção de formatação em colunas")    
    cols01 = st.columns(2)    
    cols01[0].write('Texto da Coluna 01')
    cols01[1].write('Texto da Coluna 02')
elif choice == "Texto_Markdown":
    st.subheader("Texto Markdown")
    st.write("Veja a seguir opção de formatação de texto Markdown")
    st.markdown(
    """
    ## *Alguns sites referências*:    
    - [Streamlit: hello world](https://calmcode.io/streamlit/hello-world.html)
    - [:star: Streamlit emoji shortcodes](https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlitapp.com/)
    - [Layouts and Containers](https://docs.streamlit.io/library/api-reference/layout)
   
    ##### CRONOGRAMA
    DIA | CH HORÁRIA | CONTEÚDO
    :---------: | :------: | :-------:
    Dia 1 de 2 | ?h | ? a ?
    Dia 2 de 2 | ?h | ? a ?
    """
    )
elif choice == "Inserir_Figura":
    st.image(image01, width=800, caption='Rótulo da Imagem 01') 
    
