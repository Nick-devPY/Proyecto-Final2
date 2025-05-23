from pymongo import MongoClient as mongo_client
from django.conf import settings


def conectar_db():
    """Conecta a la base de datos MongoDB y devuelve el cliente y la base de datos."""
    # Configuración de la conexión a la base de datos
    cliente = mongo_client(
        settings.MONGODB_CONFIG["HOST"], settings.MONGODB_CONFIG["PORT"]
    )
    db = cliente[settings.MONGODB_CONFIG["DB_NAME"]]
    coleccion = db["trabajos"]
    return coleccion
