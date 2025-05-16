import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# 1) Carga las variables de entorno de tu .env
load_dotenv()

# 2) Construye el diccionario con la info de tu service account
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

# 3) Inicializa la app de Firebase con esas credenciales
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)

# 4) Obtén el cliente de Firestore
db = firestore.client()

# 5) Escribe un documento en tu colección
data = {
    "nombre": "Juan",
    "edad": 30,
    "cargo": "Ingeniero"
}

# a) Si quieres un ID aleatorio:
doc_ref = db.collection("mi_coleccion").add(data)


# b) Si prefieres un ID específico:
db.collection("mi_coleccion").document("usuario_juan").set(data)
print("Documento 'usuario_juan' creado/actualizado")
