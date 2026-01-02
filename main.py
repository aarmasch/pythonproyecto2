import requests
from tabulate import tabulate
import mysql.connector

    

URL = 'https://restcountries.com/v3.1/region/America'

response = requests.get(URL)

if response.status_code == 200:
    print('conexión a api exitosa')
    data = response.json()
    rows = []
    for pais in data:
        nombre = pais['name']['common']
        capital = pais['capital'][0]
        region = pais['region']
        population = pais['population']
        rows.append([nombre,capital,region,population])

    headers = ['Nombre','Capital','Región','Población']
    print(tabulate(rows,headers,tablefmt='grid'))
    
    # CARGAMOS DATA EN LA BASE DE DATOS
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='proyecto2'
    )
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS pais(
            id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(255) NOT NULL,
            capital VARCHAR(255) NOT NULL,
            region VARCHAR(255),
            poblacion BIGINT
            );
            """
        )
        #INSERTAMOS LOS USUARIOS A LA BD
        for pais in rows:
            cursor.execute(
                """
                insert into pais(nombre,capital,region,poblacion)
                values(%s,%s,%s,%s)
                """,
                pais
            )
        connection.commit()
        connection.close()
        print(f' Registros importados a la base de datos')
    else:
        print('Error al conectarse a la base de datos')
else:
    print(f'error : {response.status_code}')