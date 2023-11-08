from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
import re
import pandas as pd
import numpy as np

def extract_flight_data(origins, destinations, startdates):
    flight_data = {
        "Origin": [],
        "Destination": [],
        "StartDate": [],
        "DepartureTime": [],
        "ArrivalTime": [],
        "Price": [],
        "Airline": [],
        "Stops": [],
        "LayoverAirports": [],
        "TravelTime": [],
        "ClassType": []
    }

    # Set Chrome options and the user-agent
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

    # Initialize the ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    for origin in origins:
        for destination in destinations:
            for startdate in startdates:
                url = f"https://www.kayak.cl/flights/{origin}-{destination}/{startdate}?sort=bestflight_a"
                # Open the Kayak website
                driver.get(url)

                # Presionar multiples veces 'ver mas resultaods' para obtener la mayor cantidad de vuelos posibles por búsqueda
                while True:
                    try:
                        boton = WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and @class="ULvh-button show-more-button"]'))
                        boton.click()
                    except:
                        print("Button disappeared or not clickable. Stopping.")
                        break

                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Extraer Horarios de salida y llegada
                deptime = []
                arrtime = []
                div_elements_times = soup.find_all('div', class_='vmXl vmXl-mod-variant-large')

                for div in div_elements_times:
                    spans = div.find_all('span')
                    if len(spans) == 3:
                        deptime.append(spans[0].get_text())
                        arrtime.append(spans[2].get_text())

                # Extraer todos los precios
                prices_int = []
                div_elements_price = soup.find_all('div', class_='f8F1-price-text')

                for div in div_elements_price:
                    price_text = div.get_text()
                    price_text = price_text.replace('$', '').replace('.', '')
                    prices_int.append(int(price_text))

                # Extraer lineas aereas
                lineas = []
                div_elements_lineas = soup.find_all('div', class_='J0g6-operator-text')

                for div in div_elements_lineas:
                    lineas_text = div.get_text()
                    lineas.append(lineas_text)

                # Extraer lineas aereas
                escalas = []
                span_elements_escalas = soup.find_all('span', class_='JWEO-stops-text')

                for div in span_elements_escalas:
                    escalas_text = div.get_text()
                    escalas.append(escalas_text)

                # Extraer aeropuertos de escalas
                cleaned_airport_codes = []
                div_elements_jweo = soup.find_all('div', class_='JWEO')

                for div_jweo in div_elements_jweo:
                    div_airport = div_jweo.find('div', class_='c_cgF c_cgF-mod-variant-full-airport')
                    span_elements = div_airport.find_all('span')
                    airport_codes = [span.get_text() for span in span_elements]
                    cleaned_airport_code = ', '.join(set(filter(None, airport_codes)))
                    cleaned_airport_codes.append(cleaned_airport_code)

                cleaned_airport_codes = [', '.join(set(code.split(', '))) for code in cleaned_airport_codes]

                # Extraer horas del viaje
                horas_viaje = []
                div_elements_horas = soup.find_all('div', class_='xdW8 xdW8-mod-full-airport')

                for div in div_elements_horas:
                    horas_text = div.find('div', class_='vmXl vmXl-mod-variant-default').get_text()
                    horas_viaje.append(horas_text)

                # Extraer tipo de clase
                tipo_clase = []
                div_M_JD = soup.find_all('div', class_='M_JD')

                for div in div_M_JD:
                    div_aC3z_links = div.find('div', class_='aC3z-links')
                    div_aC3z_option = div_aC3z_links.find('div', class_='aC3z-option')
                    div_aC3z_name = div_aC3z_option.find('div', class_='aC3z-name').get_text()
                    tipo_clase.append(div_aC3z_name)

                # Agregar los datos a la estructura de datos
                for i in range(len(deptime)):
                    flight_data["Origin"].append(origin)
                    flight_data["Destination"].append(destination)
                    flight_data["StartDate"].append(startdate)
                    flight_data["DepartureTime"].append(deptime[i])
                    flight_data["ArrivalTime"].append(arrtime[i])
                    flight_data["Price"].append(prices_int[i])
                    flight_data["Airline"].append(lineas[i])
                    flight_data["Stops"].append(escalas[i])
                    flight_data["LayoverAirports"].append(cleaned_airport_codes[i])
                    flight_data["TravelTime"].append(horas_viaje[i])
                    flight_data["ClassType"].append(tipo_clase[i])

    # Cerrar el navegador al finalizar
    driver.quit()

    return flight_data

# Definir las listas de origen, destino y fechas
origins = ['SCL', 'MXP', 'ZRH', 'FRA']
destinations = ['SCL', 'MXP', 'ZRH', 'FRA']
startdates = ["2023-12-11", "2023-12-12", "2023-12-13"]

# Llamar a la función para extraer datos
flight_data = extract_flight_data(origins, destinations, startdates)

# Convertir los datos a un DataFrame de Pandas
df = pd.DataFrame(flight_data)

# Imprimir el DataFrame
print(df)



