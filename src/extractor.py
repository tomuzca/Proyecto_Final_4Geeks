from dotenv import load_dotenv
import os
import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd 
from tqdm import tqdm
import time 

load_dotenv()


client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret), requests_timeout=10, retries=10)

generos = ["rock", "pop", "hip-hop", "jazz", "electronic", "country", "reggae", "metal", "classical", "blues"]
año_inicial = 1950
año_final = 2023

# Crear una lista de DataFrames para cada género
dfs = []

# Itera sobre los géneros
for genero in generos:
    offset = 0
    pbar = tqdm(total=50)  # Inicializa la barra de progreso para cada género
    
    genre_data = []
    
    while True:
        try:
            resultados = sp.search(q=f'genre:"{genero}" year:{año_inicial}-{año_final}', type='track', limit=50, offset=offset)
            
            if not resultados['tracks']['items']:
                break  # No hay más resultados
            
            for track in resultados['tracks']['items']:
                nombre_canción = track['name']
                artistas = [artista['name'] for artista in track['artists']]
                id_canción = track['id']
                
                # Obtiene las características de la canción
                caracteristicas = sp.audio_features([id_canción])[0]
                
                # Obtiene el análisis de audio de la canción
                analisis_audio = sp.audio_analysis(id_canción)
                
                # Crea un diccionario con los datos de la canción
                row = {
                    "Género": genero,
                    "Canción": nombre_canción,
                    "Artistas": ", ".join(artistas),
                    "Temperatura de baile": caracteristicas["danceability"],
                    "Energía": caracteristicas["energy"],
                    "Duración": caracteristicas["duration_ms"],
                    "Key": caracteristicas["key"],
                    "Mode": caracteristicas["mode"],
                    "Time Signature": caracteristicas["time_signature"],
                    "Acousticness": caracteristicas["acousticness"],
                    "Danceability": caracteristicas["danceability"],
                    "Instrumentalness": caracteristicas["instrumentalness"],
                    "Liveness": caracteristicas["liveness"],
                    "Loudness": caracteristicas["loudness"],
                    "Speechiness": caracteristicas["speechiness"],
                    "Valence": caracteristicas["valence"],
                    "Tempo": caracteristicas["tempo"]
                }
                
                for key, value in analisis_audio.items():
                    if isinstance(value, (int, float)):
                        row[key] = value
                
                genre_data.append(row)
                pbar.update(1)  # Actualiza la barra de progreso
            
            offset += 50  # Incrementa el offset para la siguiente página de resultados
        except Exception as e:
            print(f"Error: {e}")
            print("Esperando 60 segundos para evitar la limitación de la API...")
            time.sleep(60)
    
    # Convierte la lista de diccionarios en un DataFrame para el género actual
    df_genre = pd.DataFrame(genre_data)
    dfs.append(df_genre)
    
    pbar.close()  # Cierra la barra de progreso al final de cada género

# Concatena todos los DataFrames en uno solo
df = pd.concat(dfs, ignore_index=True)

df.info()