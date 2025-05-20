import random
import os
from openai import OpenAI
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")
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
if not api_key:
    raise ValueError("La variable de entorno OPENAI_API_KEY no está definida.")


client = OpenAI(api_key=api_key)
coco_classes = [
    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard',
    'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
    'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork',
    'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange',
    'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair',
    'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv',
    'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave',
    'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase',
    'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

ages = [8,9,10,11,12,13,14]
moods = ['happy', 'sad', 'angry', 'normal','relaxed']
genders = ['male','female']
names = ['Lucas', 'Mateo', 'Santiago', 'Valentina', 'Emilia', 'Isabella', 'Camila', 'Sofia', 'Victoria', 'Renata']

def generate_random_data():
    """
    Generate random data for testing.
    """
    data_promt = {
        'class': random.choice(coco_classes),
        'age': random.choice(ages),
        'mood': random.choice(moods),
        'gender': random.choice(genders),
        'name': random.choice(names),
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "created_at": firestore.SERVER_TIMESTAMP,
        'result': '',
    }
    prompt =  f'''
                        Generate an explanatory paragraph in spanish adapted for a child named {data_promt['name']} diagnosed with Autism Spectrum Disorder (ASD), about the word "{data_promt["class"]}".
                        The child is {data_promt["age"]} years old, {data_promt["gender"]}, and currently feeling {data_promt["mood"]}.
                        Use simple, clear, and concrete language. Help the child understand what the word means and how it relates to their daily life. Give examples that make sense for a child of that age and emotional state.
                        The explanation should be friendly and supportive. Please give a direct explanation — do not include placeholders or fields in brackets like [name]
                        **Limit the explanatory paragraph to no more than 80 words.**
                        '''
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    )
    data_promt['result'] = response.choices[0].message.content
    return data_promt

def save_in_db(data):
    """
    Save the generated data in a database or file.
    """
    db.collection("inferences").add(data)


for i in range(1):
    result = generate_random_data()
    save_in_db(result)
    print(result)
