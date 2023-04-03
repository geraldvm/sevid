import OCR
from PIL import Image

ocr = OCR()
imgIn = Image.open("resources/t.jpg")
imgOut,text = ocr.recognizeText(imgIn)
ocr.save_text(text,"text-outout.txt")
lista =ocr.save_text_list(text)
print(lista)
imgOut.show()
imgOut.save("img-out/out.jpg")
