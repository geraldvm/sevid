import base64
from OCR import OCR
from flask import Flask, jsonify, request
from io import BytesIO
from PIL import Image


app = Flask(__name__)

@app.route('/recognize-text', methods=['POST'])
def recognize_text():
    # Obtenemos la imagen del request
    #img = request.files['image'].read()
    #img = Image.open(io.BytesIO(img))
    # Obtener la imagen enviada en la solicitud
    image_file = request.files.get('image','')
    image = Image.open(image_file)

    # Procesamos la imagen con OCR
    ocr = OCR()
    image, text = ocr.recognizeText(image)

    # Convertimos la imagen a bytes para enviarla en la respuesta
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    img_str = base64.b64encode(buffer.getvalue()).decode("ascii")

 
    print(ocr.save_text_list(text))
    # Devolvemos la respuesta como JSON
    return jsonify({
        'image': img_str,
        'text': ocr.save_text_list(text)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)