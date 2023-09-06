# Utilisez l'image de base Python
FROM python:3.11-slim
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 libgl1 -y
# Définissez le répertoire de travail dans l'image
WORKDIR /

# Copiez le code de l'application Flask dans le conteneur
COPY . .

# Installez les dépendances nécessaires
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exposez le port sur lequel l'application Flask écoute
EXPOSE 80

# Commande pour exécuter l'application Flask lorsque le conteneur est démarré "uvicorn app.main:app --reload"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
