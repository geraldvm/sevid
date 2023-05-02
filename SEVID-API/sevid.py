"""
Copyright 2023 Gerald Valverde Mc kenzie | McKode Development

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from io import BytesIO
from json import JSONDecodeError
import time
import requests
from PIL import Image
from flask import Flask, jsonify, request

class SEVID_API:
    def __init__(self, esp32_address,ocr_address, verificator_address ):
        self.url_esp32 = f"http://{esp32_address}"
        self.url_ocr_api = ocr_address
        self.url_verificator_api = verificator_address


    def capture(self):
        # Hacer la solicitud HTTP al ESP32
        print("Capturing...")
        response = requests.get(self.url_esp32 + '/capture')
        print(response)

    def send_verification_command(self, status):
        # Hacer la solicitud HTTP al ESP32
        print("Sending result...")
        if (status):
            response = requests.get(self.url_esp32 + '/verified')
        else:
            response = requests.get(self.url_esp32 + '/not-verified')
        print(response)

    def start(self):
        # Take a photo
        self.capture()
        # Wait that photo was take it
        time.sleep(3)
        # Get image from ESP
        image = self.get_image()
        # Analyze image
        self.send_ocr(image)
             
    def send_ocr(self, filename):
        print("Analyzing OCR")
        # Creamos el payload con la imagen
        #filename = 'a.jpg'
        with open(filename, 'rb') as f:
            payload = {'image': f}
            # Enviamos la petición POST con la imagen en el payload
            response = requests.post(self.url_ocr_api + '/recognize-text', files=payload)
            # Imprimimos la respuesta
            return response.json()
        
    def verificate_id(self, data_list):
        print("Verification...")
        form_data = {
            'text':','.join(data_list)
        }
        response = requests.post(self.url_verificator_api + '/verify', data=form_data)
        # Imprimimos la respuesta
        #print(response.json())
        try:
            json_response = response.json()
            return json_response
        except JSONDecodeError as e:
            print(f"Error decodificando respuesta: {e}")
            json_response = None
            return json_response
        
        
    def get_image(self):
        # Hacer la solicitud HTTP al ESP32
        time.sleep(5)
        print("Getting...")
        response = requests.get(self.url_esp32 + '/picture')
        # Si la solicitud fue exitosa (código 200)
        if response.status_code == 200:
            # Obtener la imagen de la respuesta
            image_bytes = response.content
            # Cargar la imagen usando Pillow
            image = Image.open(BytesIO(image_bytes))
            return image
        else:
            print('Error al obtener la imagen:', response.status_code)
            return None
    
    def save_image(self, image, img_path):
        time.sleep(1)
        print("Saving...")
        # Guardar la imagen en el disco
        image.save(img_path)

# Ejemplo de uso
"""
direccion_ip_esp32 = "192.168.100.2"
esp32_imagen = SEVID_API(direccion_ip_esp32)
esp32_imagen.capture()
time.sleep(3)
image = esp32_imagen.get_image()
esp32_imagen.save_image(image, 'images/t.jpg')
"""

app = Flask(__name__)

@app.route('/start', methods=['GET'])
def start_process():
    ip_address_esp32 = "172.20.10.9"
    url_address_ocr_api='http://localhost:5000'
    url_address_verification_api='http://localhost:3030'
    api = SEVID_API(ip_address_esp32,url_address_ocr_api,url_address_verification_api)
    # Take photo
    api.capture()
    
    # Get image from ESP
    image = api.get_image()
    # Save image
    filename = "images/id.jpg"
    api.save_image(image,filename)
    # Analyze image
    filename = "images/test.jpg"
    ocr_result = api.send_ocr(filename)
    print(ocr_result['text'])
    response = api.verificate_id(ocr_result['text'])
    api.send_verification_command(response["Status"])

    #response= api.send_verification_command(False)
    return response

if __name__ == '__main__':
    app.run(debug=True, port=8000)