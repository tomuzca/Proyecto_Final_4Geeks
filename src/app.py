import streamlit as st
import numpy as np
import pandas as pd
import requests
from io import BytesIO
import pickle
from pickle import load
from datetime import datetime
import gdown  # Agrega la importación de la biblioteca gdown

# ID del archivo en Google Drive
file_id = '1Iz-IR0WETEt1y1LCnCwUDN5bpIIB1EuU'
destination = 'random_forest_regressor_default_42.pkl'

# Descargar el modelo desde Google Drive
gdown.download(f'https://drive.google.com/uc?id={file_id}', destination, quiet=False)

# Cargar el modelo desde el archivo descargado
with open(destination, 'rb') as file:
    model = pickle.load(file)

# Load DataFrame with distances
distances_df = pd.read_pickle('millas') 
distances_df['Distance (miles)'] = distances_df['Distance (miles)'].astype(float)# Reemplaza 'tu_dataframe_con_distancias.csv' con el nombre de tu archivo CSV

# List of destinations
destinos = distances_df['Destination'].tolist()

# List of airlines
aerolineas = ['Copa Airlines', 'LATAM Airlines', 'Delta', 'Avianca', 'JetSMART',
              'Arajet', 'American Airlines', 'United Airlines',
              'Varias aerolíneas', 'Aeromexico', 'Sky Airline', 'Air Canada',
              'Aerolineas Argentinas', 'Hahn Air', 'KLM', 'Iberia',
              'British Airways', 'Vueling', 'LEVEL', 'Air Europa',
              'LATAM Airlines Peru', 'Air France', 'Turkish Airlines', 'WestJet',
              'Qantas Airways', 'Finnair', 'Qatar Airways', 'ITA Airways',
              'Malaysia Airlines', 'ANA', 'Cathay Pacific', 'Korean Air']

st.title("Bienvenido")
st.text("Tu estimador de pasajes para salir de Santiago ")

fecha_viaje = st.date_input("Fecha que quieres viajar")
fecha_hoy = datetime.now().date()

# Calcular la cantidad de días hasta la fecha de viaje
days_to_come = (fecha_viaje - fecha_hoy).days

stops = st.radio("Escalas", ["0", "1", "2", "3"])

# Destination selector
destino_seleccionado = st.selectbox('Seleccione el destino:', destinos)

# Retrieve distance for the selected destination
distance = distances_df.loc[distances_df['Destination'] == destino_seleccionado, 'Distance (miles)'].values[0]

# Airline selector
aerolinea_seleccionada = st.selectbox("Aerolinea", aerolineas)

# ClassType selector
class_type_seleccionada = st.selectbox("Clase", ["Turista", "Ejecutiva"])

# Map the selected class type to 0 or 1
class_type_mapping = {"Turista": 0, "Ejecutiva": 1}
class_type_encoded = class_type_mapping[class_type_seleccionada]

# Period selector
periodo_seleccionado = st.selectbox("Periodo", ["Mañana", "Tarde", "Noche"])
periodo_mapping = {"Mañana": 0, "Tarde": 1, "Noche": 2}
periodo_encoded = periodo_mapping[periodo_seleccionado]

travel_time = stops * 10

if st.button("Calcular"):
    # Convert destination to one-hot encoding
    destino_one_hot = np.zeros(len(destinos))
    destino_one_hot[destinos.index(destino_seleccionado)] = 1

    # Convert airline to one-hot encoding
    aerolinea_one_hot = np.zeros(len(aerolineas))
    aerolinea_one_hot[aerolineas.index(aerolinea_seleccionada)] = 1

    vector_pred = [int(stops), distance, days_to_come] + list(destino_one_hot) + list(aerolinea_one_hot) + [class_type_encoded, periodo_encoded, int(travel_time)]

    # Prediction
    prediction = model.predict([vector_pred])
    st.write("El estimado de tu pasaje debe ser de", prediction)
  