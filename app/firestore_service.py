import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

db = firestore.client()

#regresa todos los usuarios
def get_users():
    return db.collection('users').get()

#regresa data de usuario (user_id)
def get_user(user_id):
    return db.collection('users').document(user_id).get()

def user_put(user_data):
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({'password':user_data.password})

#regresa los todo's de un usuario (user_id) 
def get_todos(user_id):
    return db.collection('users').document(user_id).collection('todos').get()

def put_todo(user_id, description):
    todos_collections_ref = db.collection('users').document(user_id).collection('todos')
    todos_collections_ref.add({'description':description, 'done':False})

def delete_todo(user_id, todo_id):
    #forma normal
        #todo_ref = db.collection('users').document(user_id).collection('todos').document(todo_id)
    #otra forma de llegar a la ruta de la base de datos
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.delete()

def update_todo(user_id, todo_id, done):
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.update({'done': not done})

def _get_todo_ref(user_id, todo_id):
    return db.document('users/{}/todos/{}'.format(user_id,todo_id))