from utils.db import db
from fastapi.responses import JSONResponse
from schemas.user_schema import SchemaUser, SchemaContact,SchemaContacts,SchemaUsers,schemasMerges,SchemaMergeUser
from schemas.schema_permisos import SchemaPermisos,SchemaPermiso
from fastapi.responses import JSONResponse
from passlib.hash import sha256_crypt
from bson import ObjectId
from middlewares.auth_middleware import write_token
from pymongo import MongoClient
from datetime import datetime

def nuevo_usuario(usuario):
    usuario = dict(usuario)
    user = db.Users.find_one({"correo":usuario["correo"]})
    if user :
        return JSONResponse(content="El usuario ya existe", status_code=400)
    usuario["contraseña"] = sha256_crypt.encrypt(usuario["contraseña"])
    nuevo_usuario = db.Users.insert_one(usuario).inserted_id
    ususario_insertado= db.Users.find_one({"_id":nuevo_usuario})
    return JSONResponse(content=SchemaUser(ususario_insertado), status_code=201)

def get_all_users():
    users = db.Users.find()
    list_users = list(users)
    return JSONResponse(content=SchemaUsers(list_users), status_code=200)

def get_all_contacts(email):
    user_log = db.Users.find_one({"correo":email["correo"]})
    user_log= dict(user_log)
    # Construye la cadena de conexión
    connection_string = user_log["url"] 
    # Conecta a MongoDB Atlass
    client = MongoClient(connection_string)
    # Selecciona la base de datos
    db_user = client["Usuario"]
    list_contacts =db_user.contactos.find()
    list_contacts = list(list_contacts)
    return JSONResponse(content=SchemaContacts(list_contacts), status_code=200)

def nuevo_contacto(email,contact):
    user_log = db.Users.find_one({"correo":email["correo"]})
    user_log= dict(user_log)
    contact=dict(contact)
    contact["direccion"] = dict(contact["direccion"])
    fecha_insertado=datetime.now()
    contact["dia_creado"]= fecha_insertado.strftime("%Y-%m-%d %H:%M:%S")
    # Construye la cadena de conexión
    connection_string = user_log["url"] 
    # Conecta a MongoDB Atlass
    client = MongoClient(connection_string)

    # Selecciona la base de datos
    db_user = client["Usuario"]
    nuevo_usuario = db_user.contactos.insert_one(contact).inserted_id
    ususario_insertado= db_user.contactos.find_one({"_id":nuevo_usuario})
    return JSONResponse(content=SchemaContact(ususario_insertado), status_code=201)

def login(user):
    user_auth = db.Users.find_one({"correo": user["correo"]})

    if not user_auth:
        return JSONResponse(status_code=400, content={
            "status": "Credentials invalids!"})

    # valid Password
    password = sha256_crypt.verify(user["contraseña"], user_auth["contraseña"])
    
    if not password:
        return JSONResponse(status_code=400, content={
            "status": "Credentials invalids!"})

    # Generate token
    token = write_token(user)
    return JSONResponse(content={"token": token, "status": "Succes Session!"}, status_code=201)

def solicitar_merge(datos_permiso,email):
    print("solicita")
    print(email["correo"])
    print("recibe")
    if datos_permiso["email_destinatario"] == email["correo"]:
        print("Denegando permiso")
        return JSONResponse(content={"error":"No puedes hacer merge con tu propia agenda"}, status_code=400)
    
    user_log = db.Users.find_one({"correo":datos_permiso["email_destinatario"]})
    user_log= dict(user_log)
    # Construye la cadena de conexión
    connection_string = user_log["url"] 
    # Conecta a MongoDB Atlass
    client = MongoClient(connection_string)
    # Selecciona la base de datos
    db_user = client["Usuario"]
    list_permisos = db_user.permisos.find()
    list_permisos = list(list_permisos)
    if len(list_permisos) ==0:
        db_user.permisos.insert_one({"user_solicita":email["correo"], "lectura/escritura":False,"merge":False, "status":False}).inserted_id
    return JSONResponse(content={"Succes":"Se solicito permiso con exito"}, status_code=201)

def permisos_usuario(email):
    user_log = db.Users.find_one({"correo":email["correo"]})
    user_log= dict(user_log)
    # Construye la cadena de conexión
    connection_string = user_log["url"] 
    # Conecta a MongoDB Atlass
    client = MongoClient(connection_string)
    # Selecciona la base de datos
    db_user = client["Usuario"]
    list_permisos =db_user.permisos.find()
    list_permisos = list(list_permisos)
    return JSONResponse(content=SchemaPermisos(list_permisos), status_code=200)

def agenda_user(email, user_permiso):

    """
    Visulizar todos los contactos de otro usuario
    """
    user_agenda = db.Users.find_one({"correo":email})
    user_agenda= dict(user_agenda)
    # Construye la cadena de conexión
    connection_string = user_agenda["url"] 
    print(connection_string)
    # Conecta a MongoDB Atlass
    client = MongoClient(connection_string)
    # Selecciona la base de datos
    db_user = client["Usuario"]
    permisos = db_user.permisos.find_one({"user_solicita":user_permiso["correo"]})
    if permisos["lectura/escritura"]== False:
         return JSONResponse(content="No tienes permiso de Lectura", status_code=200)
    list_contacts = db_user.contactos.find()
    list_contacts = list(list_contacts)
    return JSONResponse(content=SchemaContacts(list_contacts), status_code=200)

def esta_permiso_merge(email, user_permiso):
    user_agenda = db.Users.find_one({"correo":email})
    user_agenda= dict(user_agenda)
    # Construye la cadena de conexión
    connection_string = user_agenda["url"] 
    print(connection_string)
    # Conecta a MongoDB Atlass
    client = MongoClient(connection_string)
    # Selecciona la base de datos
    db_user = client["Usuario"]
    permisos = db_user.permisos.find_one({"user_solicita":user_permiso["correo"]})
    if permisos["merge"]== False:
         return JSONResponse(content="No tienes permiso de merge", status_code=400)
    return JSONResponse(content={"status":"si tines permiso"}, status_code=200)
    
    
def aceptar_permisos_lectura(id_permiso,email):
    user_agenda = db.Users.find_one({"correo":email["correo"]})
    user_agenda= dict(user_agenda)
    # Construye la cadena de conexión
    connection_string = user_agenda["url"] 
    print(connection_string)
    # Conecta a MongoDB Atlass
    client = MongoClient(connection_string)
    # Selecciona la base de datos
    db_user = client["Usuario"]
    db_user.permisos.update_one({"_id":ObjectId(id_permiso)}, {"$set":{"lectura/escritura":True}})
    permiso_lectura = db_user.permisos.find_one({"_id":ObjectId(id_permiso)})
    return JSONResponse(content=SchemaPermiso(permiso_lectura), status_code=200)


def aceptar_permisos_merge(id_permiso,email):
    user_agenda = db.Users.find_one({"correo":email["correo"]})
    user_agenda= dict(user_agenda)
    # Construye la cadena de conexión
    connection_string = user_agenda["url"] 
    print(connection_string)
    # Conecta a MongoDB Atlass
    client = MongoClient(connection_string)
    # Selecciona la base de datos
    db_user = client["Usuario"]
    db_user.permisos.update_one({"_id":ObjectId(id_permiso)}, {"$set":{"merge":True,"status":True}})
    permiso_lectura = db_user.permisos.find_one({"_id":ObjectId(id_permiso)})
    return JSONResponse(content=SchemaPermiso(permiso_lectura), status_code=200)

def aceptar_todo(id_permiso,email):
    user_agenda = db.Users.find_one({"correo":email["correo"]})
    user_agenda= dict(user_agenda)
    # Construye la cadena de conexión
    connection_string = user_agenda["url"] 
    print(connection_string)
    # Conecta a MongoDB Atlass
    client = MongoClient(connection_string)
    # Selecciona la base de datos
    db_user = client["Usuario"]
    db_user.permisos.update_one({"_id":ObjectId(id_permiso)}, {"$set":{"lectura":True,"escritura":True,"merge":True, "status":True}})
    permiso_lectura = db_user.permisos.find_one({"_id":ObjectId(id_permiso)})
    return JSONResponse(content=SchemaPermiso(permiso_lectura), status_code=200)


def hacer_merge(datos_merge, email_log):
    # Traemos url de conexion del ususario con quien haremos el merge
    user_merge = db.Users.find_one({"correo":datos_merge["email_destinatario"]})
    user_merge= dict(user_merge)
    # Construye la cadena de conexión
    connection_string = user_merge["url"] 
    print(connection_string)
    # Conecta a MongoDB Atlass
    client = MongoClient(connection_string)
    # Selecciona la base de datos
    db_user_merge = client["Usuario"]
    list_contacts_user_merge = db_user_merge.contactos.find()
    list_contacts_user_merge = list(list_contacts_user_merge)
    for contact  in list_contacts_user_merge:
        contact["_id"] = str(contact["_id"])

    # Traemos url de conexion del ususario con ususario Logeodo
    user_logeado = db.Users.find_one({"correo":email_log["correo"]})
    user_logeado= dict(user_logeado)
    # Construye la cadena de conexión
    connection_string = user_logeado["url"] 
    print(connection_string)
    # Conecta a MongoDB Atlass
    client = MongoClient(connection_string)
    # Selecciona la base de datos
    db_user_logeado = client["Usuario"]
    list_contacts_user_logeado = db_user_logeado.contactos.find()
    list_contacts_user_logeado = list(list_contacts_user_logeado)
    for contact  in list_contacts_user_logeado:
        contact["_id"] = str(contact["_id"])

    if datos_merge["tipo_merge"] == "Todos":
        list_merge = iniciar_merge_todos(list_contacts_user_logeado,list_contacts_user_merge,db_user_logeado,datos_merge["email_destinatario"])
        return JSONResponse(content={"contacts":SchemaMergeUser(list_merge)}, status_code=201)
    else :
        print("hice merge todos los contacos actuales")
        iniciar_merge_mas_actual(list_contacts_user_logeado, list_contacts_user_merge, db_user_logeado)



def iniciar_merge_todos(list_contacts_user_logeado,list_contacts_user_merge,db_user_logeado,datos_merge):
    list_agendas_merge = list_contacts_user_logeado + list_contacts_user_merge
    exist_merge = db_user_logeado.agendas_merge.find({"usuario_merge":datos_merge})
    exist_merge = list(exist_merge)
    if len(exist_merge) ==0:
        id_merge = db_user_logeado.agendas_merge.insert_one({"usuario_merge":datos_merge, "contacts":list_agendas_merge}).inserted_id
        list_merge = db_user_logeado.agendas_merge.find_one({"_id":id_merge})
        return list_merge
    else:
        merge = exist_merge[0]
        db_user_logeado.agendas_merge.update_one({"_id":merge["_id"]}, {"$set":{"contacts":list_agendas_merge}})
        list_merge = db_user_logeado.agendas_merge.find_one({"_id":merge["_id"]})
        return list_merge
    

def iniciar_merge_mas_actual(contactos_user_log, contactos_usuario_merge):
    return []
    