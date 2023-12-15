
from pymongo import MongoClient
# from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

# Reemplaza las siguientes líneas con tu información de MongoDB Atlas
username = "tu_usuario"
cluster_name = "tu_cluster_name"
database_name = "tu_database_name"
password = quote_plus('*ElIngenieroErnesto155MongoAtlas*')

# Construye la cadena de conexión
connection_string = "mongodb+srv://ernest:admin123@agenda.9tknbja.mongodb.net/"  

# Conecta a MongoDB Atlass
client = MongoClient(connection_string)

# Selecciona la base de datos
db = client["Agenda"]
 


