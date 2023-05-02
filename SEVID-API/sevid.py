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
import time
import requests
from PIL import Image
from flask import Flask, jsonify, request

class SEVID_API:
    def __init__(self, esp32_address,ocr_address ):
        self.url_esp32 = f"http://{esp32_address}"
        self.url_ocr_api = ocr_address

    def capture(self):
        # Hacer la solicitud HTTP al ESP32
        print("Capturing...")
        response = requests.get(self.url_esp32 + '/capture')
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
            print(response.json())
            return response.json()
        
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
    ip_address_esp32 = "192.168.18.21"
    url_address_ocr_api='http://localhost:5000'
    api = SEVID_API(ip_address_esp32,url_address_ocr_api)
    # Take photo
    api.capture()
    # Get image from ESP
    image = api.get_image()
    # Save image
    filename = "images/id.jpg"
    api.save_image(image,filename)
    # Analyze image
    filename = "images/test.jpg"
    response = api.send_ocr(filename)
    return response
    #return "Ok"

if __name__ == '__main__':
    app.run(debug=True, port=8000)