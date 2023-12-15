from fastapi import APIRouter,Depends
from controllers.users_controllers import get_all_contacts ,nuevo_usuario,nuevo_contacto, login,solicitar_merge,get_all_users,permisos_usuario,agenda_user,aceptar_permisos_lectura,aceptar_permisos_merge,aceptar_todo, esta_permiso_merge,hacer_merge
from models.user_model import User, Login, Contact,Permiso
from middlewares.auth_middleware import Portador 

routes_user = APIRouter()

@routes_user.post("/login")
def login_user(user:Login):
    user = dict(user)
    return login(user)

@routes_user.post("/new_user")
def new_user(user :User):
    return nuevo_usuario(user)

@routes_user.get("/getallContacts")
def get_all_contact_routes(user = Depends(Portador())):
    return  get_all_contacts(user)

@routes_user.post("/nuevo-contacto")
def nuevo_contact_routes( contacto: Contact ,user = Depends(Portador())):
    return  nuevo_contacto(dict(user), contacto)

@routes_user.get("/all_users")
def get_all_users_route():
    return get_all_users()

@routes_user.get("/all_merge")
def todos_permisos_user(user = Depends(Portador())):
    return permisos_usuario(user)

@routes_user.post("/solicitar-merge")
def nuevo_merge(datos_permiso:Permiso ,user = Depends(Portador())):
    datos_permiso = dict(datos_permiso)
    return solicitar_merge(datos_permiso, user)

@routes_user.get("/contacts_user/{email}")
def ver_agenda_usuario(email,user = Depends(Portador())):
    return agenda_user(email, user)

@routes_user.get("/permisomerge_user/{email}")
def hay_permiso_merge(email,user = Depends(Portador())):
    return esta_permiso_merge(email, user)

@routes_user.post("/hacer_merge")
def hacer_merge_route(datos_merge :Permiso,email_log = Depends(Portador())):
    datos_merge = dict(datos_merge)
    return hacer_merge(datos_merge, email_log)

@routes_user.put("/aceptar_permiso_lectura/{id_permiso}")
def aceptar_lectura(id_permiso,user = Depends(Portador())):
    return aceptar_permisos_lectura(id_permiso,user)

@routes_user.put("/aceptar_permiso_merge/{id_permiso}")
def aceptar_merge(id_permiso,user = Depends(Portador())):
    return aceptar_permisos_merge(id_permiso,user)

@routes_user.put("/aceptar_permiso_todos/{id_permiso}")
def aceptar_todos(id_permiso,user = Depends(Portador())):
    return aceptar_todo(id_permiso,user)

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb3JyZW8iOiJiZWNlZG9tQGdtYWlsLmNvbSIsImNvbnRyYXNlXHUwMGYxYSI6ImFkbWluMTIzNCIsImV4cCI6MTcwMjc0NzU2N30.jlpwqCyowYn1quRjgy6xpvsMidnrfyJBJ92xtXLD0mc