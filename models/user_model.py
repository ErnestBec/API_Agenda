from pydantic import BaseModel
from typing import Optional, Dict
class direccion(BaseModel):
    calle:str
    cuidad:str
    codigo_postal:int
    num_exterior:Optional[int]
    numero_interior:Optional[int]
    colonia:str
class User(BaseModel):
    _id:Optional[str]
    nombre: str 
    correo:str
    contraseña:str
    url:str
class Contact (BaseModel):
    _id:Optional[str]
    nombre: str
    correo:str
    telefono:int
    direccion:direccion

class Login(BaseModel):
    correo:str
    contraseña:str

class Permiso(BaseModel):
    email_destinatario:str
    tipo_merge:str