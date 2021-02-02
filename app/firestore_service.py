import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

db = firestore.client()

#regresa todos los usuarios
def get_users():
    return db.collection('users').get()

#regresa nombre de usuario (user_id)
def get_user(user_id):
    return db.collection('users').document(user_id).get()

#regresa los todo's de un usuario (user_id) 
def get_todos(user_id):
    return db.collection('users').document(user_id).collection('todos').get()