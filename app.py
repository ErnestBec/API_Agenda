from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes.users_routes import routes_user 
app = FastAPI()

load_dotenv()
 
app.add_middleware(
    CORSMiddleware,
    # Puedes especificar los orígenes permitidos en lugar de "*"
    allow_origins=["*"],
    allow_credentials=True,
    # Puedes especificar los métodos permitidos (por ejemplo, ["GET", "POST"])
    allow_methods=["*"],
    # Puedes especificar los encabezados permitidos (por ejemplo, ["Content-Type"])
    allow_headers=["*"],
) 
app.include_router(routes_user)