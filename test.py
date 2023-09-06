import requests
from io import BytesIO
from PIL import Image

# Remplacez par l'adresse de votre API
url = "http://127.0.0.1:42504/predict"

# Ouvrir et rogner l'image
image1 = Image.open("dog.jpeg")
image_rognee = image1.crop((20, 30, 50, 236))
image_vide = Image.new("RGB", (10, 10))  # Créer une image vide
images = [image1, image_rognee, image_vide]

for idx, image in enumerate(images):
    try:
        # Convertir l'image en octets
        image_bytes = BytesIO()
        image.save(image_bytes, format="JPEG")
        image_bytes.seek(0)

        files = {'file': ('image.jpg', image_bytes, 'image/jpeg')}
        response = requests.post(url, files=files)

        print("Test Image", idx + 1)
        print("Réponse:", response.status_code, response.json())
        print("=" * 50)
    except Exception as e:
        print("Erreur:", e)

url = ("http://127.0.0.1:42504/predict_image")  # Remplacez par l'URL exacte de votre API

# Ouvrez l'image en mode binaire
with open("dog.jpeg", "rb") as image_file:
    # Utilisez la méthode POST pour envoyer l'image à l'API
    response = requests.post(url, files={"file": image_file})

# Vérifiez que la requête a réussi
if response.status_code == 200:
    # Écrivez l'image reçue dans un nouveau fichier
    with open("dog_with_boxes.jpeg", "wb") as output_image_file:
        output_image_file.write(response.content)
    print("Image enregistrée avec succès ! (dog_with_boxes.jpeg)")
else:
    print(f"Échec de la requête : {response.status_code}")
