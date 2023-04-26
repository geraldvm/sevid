"""
Validación de los datos del documento de identidad con los datos del archivo de padrón.

Copyright 2023 Gerald Valverde Mc kenzie | McKode Development

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limit
"""

class Verificator:
    def __init__(self):
        self.__padronDB = "padron.txt"
        pass

    def compare_data(self, text):
        pass

    def search_data(self, user_data):
        # Nombre del archivo de texto
        filename = self.__padronDB

        # Abrir el archivo de texto en modo lectura
        with open(filename, "r") as text:
            # Leer el archivo línea por línea
            for line in text:
                # Dividir la línea en campos separados por comas
                values = line.strip().split(",")  
                # Obtener los valores relevantes de la línea
                id = values[0]
                Firstname = values[5].strip()
                SecondName1 = values[6].strip()
                SecondName2 = values[7].strip()
                
                # Verificar si los datos personales están presentes en la línea
                if id == user_data[0] and Firstname == user_data[1] and SecondName1 == user_data[2] and SecondName2 == user_data[3]:
                    return True
            else:
                return False