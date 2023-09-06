import numpy
from fastapi import FastAPI

import io
from io import BytesIO
from random import randint
from typing import List

from PIL import Image, ImageDraw, ImageFont
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from starlette.responses import StreamingResponse
from ultralytics import YOLO

app = FastAPI()

model = YOLO(f'best.pt')


class Prediction(BaseModel):
    """Modèle Pydantic pour une prédiction d'un modèle YoloV8"""
    label: str
    confidence: float
    boxes: List[float]


@app.post("/predict")
async def predict(file: UploadFile = File(...), response_model=List[Prediction]):
    # Charger l'image à partir du fichier
    image_stream = BytesIO(await file.read())
    image = Image.open(image_stream).convert("RGB")

    # Faire une prédiction
    results = model.predict(image, conf=0.25)

    predictions: List[Prediction] = []

    for result in results:
        arrays: List[numpy.ndarray] = result.boxes.data.cpu().numpy()
        for array in arrays:
            array: List = array.tolist()

            boxes = array[:4]
            confidence = round(array[4], 2)
            label = result.names[array[5]]

            prediction = Prediction(label=label, boxes=boxes, confidence=confidence)

            predictions.append(prediction)

    return {'results': predictions}


from PIL import ImageDraw, ImageFont

# ...
class_to_color = {}


def random_color():
    return randint(0, 255), randint(0, 255), randint(0, 255)


try:
    font = ImageFont.truetype("arial.ttf", size=30)  # Modifiez le chemin pour correspondre à l'emplacement de votre fichier de police
except IOError:
    font = ImageFont.load_default()  # Utilise la police par défaut si la police TTF n'est pas trouvée


@app.post("/predict_image")
async def predict_image(file: UploadFile = File(...)):
    # Charger l'image à partir du fichier
    image_stream = BytesIO(await file.read())
    image = Image.open(image_stream).convert("RGB")

    # Faire une prédiction
    results = model.predict(image, conf=0.25)

    # Dessiner les rectangles sur l'image
    draw = ImageDraw.Draw(image)
    # Pour la plupart des systèmes, cette fonte devrait fonctionner. Sinon, vous devrez spécifier le chemin vers une fonte TTF.

    for result in results:
        arrays = result.boxes.data.cpu().numpy()
        for array in arrays:
            box = array[:4]
            confidence = round(array[4], 2)
            label = result.names[array[5]]

            # Générer une couleur aléatoire pour la classe s'il n'y en a pas encore
            if label not in class_to_color:
                class_to_color[label] = random_color()

            # Récupérer la couleur associée à la classe
            color = class_to_color[label]

            # Dessiner le rectangle avec une largeur augmentée
            draw.rectangle([box[0], box[1], box[2], box[3]], outline=color, width=5)

            # Écrire le label et la confiance au-dessus du rectangle
            text = f"{label}  {confidence:.2f}"
            draw.text((box[0], box[1] - 10), text, font=font, fill=color, )

    # Convertir l'image en bytes
    image_bytes_io = io.BytesIO()
    image.save(image_bytes_io, format='JPEG')
    image_bytes = image_bytes_io.getvalue()

    return StreamingResponse(io.BytesIO(image_bytes), media_type="image/jpeg")
