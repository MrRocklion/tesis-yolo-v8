import os
import csv
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# Cargar variables de entorno
load_dotenv()

# Configuración de credenciales
service_account_info = {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN"),
}

# Inicializar Firebase
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)

db = firestore.client()

# Obtener datos
collection_name = "inferences"
docs = db.collection(collection_name).stream()

print(f"Documentos en la colección '{collection_name}':\n")
data = []
for doc in docs:
    doc_dict = doc.to_dict()
    print(f"{doc.id} => {doc_dict}")
    data.append(doc_dict)

# Guardar en CSV
if data:
    keys = sorted(set().union(*(d.keys() for d in data)))  # obtener todas las llaves únicas
    with open("inferences.csv", mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print("Datos exportados a 'inferences.csv'.")
else:
    print("No se encontraron documentos para exportar.")
