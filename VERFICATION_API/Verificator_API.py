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

import base64
from Verificator import Verificator
from flask import Flask, jsonify, request
from io import BytesIO
from PIL import Image
import json

app = Flask(__name__)

@app.route('/verify', methods=['POST'])
def recognize_id():
    # Obtener el archivo enviado en la solicitud
    
    text = request.form.get('text', '')
    
    verificator = Verificator()
    print(text)
    # Convertirla lista en el formato esperado
    data_list = verificator.process_data(text)
    print(data_list)
    # Comparamos los datos
    
    status = verificator.search_data(data_list)
    print(status)
    # Devolvemos la respuesta como JSON
    return jsonify({
        'Status': status
    })

@app.route('/test', methods=['GET'])
def test():
    verificator = Verificator()
    # Comparamos los datos
    
    status = verificator.search_data(['116930713', 'GERALD DELROY', 'VALVERDE'])
    print(status)
    # Devolvemos la respuesta como JSON
    return jsonify({
        'Status': status
    })

if __name__ == '__main__':
    app.run(debug=True, port=3030)