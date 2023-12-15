from pydantic import BaseModel
from typing import Optional, Dict
class direccion(BaseModel):
    calle:str
    cuidad:str
    codigo_postal:int
    num_exterior:Optional[int]
    numero_interior:Optional[int]
    colonia:str

class Contact (BaseModel):
    _id:Optional[str]
    nombre: str
    correo:str
    telefono:int
    direccion:direccion



class direccionUpdate(BaseModel):
    calle:Optional[str]
    cuidad:Optional[str]
    codigo_postal:Optional[int]
    num_exterior:Optional[int]
    numero_interior:Optional[int]
    colonia:Optional[str]

class ContactUpdate(BaseModel):
    _id:Optional[str]
    nombre: Optional[str]
    correo:Optional[str]
    telefono:Optional[int]
    direccion:Optional[direccion]

class User(BaseModel):
    _id:Optional[str]
    nombre: str 
    correo:str
    contraseña:str
    url:str
    

class Login(BaseModel):
    correo:str
    contraseña:str

class Permiso(BaseModel):
    email_destinatario:str
    tipo_merge:str