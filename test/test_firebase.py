import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore


load_dotenv()


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


cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)

db = firestore.client()

data = {
    "nombre": "Juan",
    "edad": 30,
    "cargo": "Ingeniero"
}


doc_ref = db.collection("mi_coleccion").add(data)



db.collection("mi_coleccion").document("usuario_juan").set(data)
print("Documento 'usuario_juan' creado/actualizado")
