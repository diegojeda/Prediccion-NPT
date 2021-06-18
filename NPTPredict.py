import streamlit as st
import pandas as pd
from pycaret.regression import load_model, predict_model
from PIL import Image

DATE_TIME = "date/time" 

DATA_URL = "https://raw.githubusercontent.com/diegojeda/Prediccion-NPT/main/Base_Limpia.csv"

st.title("Dashboard Para Prediccion")
st.header("Horas De NPT Al Perforar Un Pozo En Campo Reds")
st.markdown("""Esta aplicación te permite generar una predicción de las horas de NPT que tendrá un pozo perforado en el campo Reds,
            teniendo en cuenta parámetros direccionales, de fluidos, tipo de pozo y duración planeada""")

@st.cache
def load_data():
    data = pd.read_csv(DATA_URL)
    return data

data=load_data() 
# Definimos la Sidebar

image1 = Image.open('Halliburton.jpg')
st.sidebar.image(image1)

st.sidebar.title("Selecciona Los Parámetros De Su Pozo")

SB_Pozo = st.sidebar.selectbox(
    'Tipo De Pozo',
    ( 'VERTICAL','DESVIADO T','TIPO J','TIPO S',"HORIZONTAL")
    )

SL_BHA = st.sidebar.slider(
    'Numero De BHAs Planeados',
    0, 50, 10
    )

SL_MW = st.sidebar.slider(
    'Media Del Peso Del Lodo Durante La Perforación Del Pozo(ppg)',
    3.0, 20.0, 9.8
    )

Duracion = st.sidebar.number_input('Numero de Días Planeados Para El Pozo',
                                   min_value=1,value=10,max_value=50)
    
MD = st.sidebar.number_input('MD (ft) Final Del Pozo',
                             min_value=1000,value=8000,max_value=15000)
                     
TVD = st.sidebar.number_input('TVD (ft) Final Del Pozo',
                              min_value=1000,value=8000,max_value=15000)

DLS_Mean = st.sidebar.number_input('DLS Medio De Todo El Pozo (Deg/100 ft)',
                                   min_value=0,value=1,max_value=5)

Azi_Mean = st.sidebar.number_input('Azimuth Medio De Todo El Pozo (Deg)',
                                   min_value=0,value=300,max_value=360)

Azi_Max = st.sidebar.number_input('Azimuth Máximo De Todo El Pozo (Deg)',
                                  min_value=0,value=300,max_value=360)

Inc_Max = st.sidebar.number_input('Inclinacion Máxima De Todo El Pozo (Deg)',
                                  min_value=0,value=3,max_value=100)


# Comenzamos con el tratamiento de la data de entrada

Data = pd.DataFrame( {"Num BHA": SL_BHA,
                      "MD": MD,
                      "TVD": TVD,
                      "DLS Mean": DLS_Mean,
                      "Azi Mean": Azi_Mean,
                      "Inc Max" : Inc_Max,
                      "Azi Max": Azi_Max,
                      "MW": SL_MW,
                      "Duracion": Duracion*24,
                      "Tipo Pozo": SB_Pozo,
                      },
                    index=[0]
                    )


# load the model from disk
model = load_model('Model_NPT')

# Realizar la Prediccion
y_pred = predict_model(model,data=Data).Label
st.subheader("El NPT Total De Tu Pozo Será: %.3f (Hrs)" % y_pred)

image = Image.open('Image.jpg')

st.image(image)