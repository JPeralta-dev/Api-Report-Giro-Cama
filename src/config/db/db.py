## Director medico diego salazar necesita tablero de facturacion de ciruguias.

# tablero de cirugia facturacion Ordenes de servicio
from sqlalchemy import Engine, create_engine,text
from typing import Optional
from src.config.env.env import settings
import logging

class DataBase():
    _instance = None
    _engine: Optional[Engine] = None
    _sessionLocal = None
    
    def get_connection_string(self) -> str:
        connection_string = (
        f"mssql+pyodbc://{settings.DB_USER}:{settings.DB_PASSWORD}"
        f"@{settings.DB_SERVER}/{settings.DB_NAME}"
        ##f"?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
    )
        return connection_string
    @classmethod
    def get_instance(cls,self) -> Engine :
        if cls._engine is None:
            cls._engine = create_engine(self.get_connection_string())
        cls._instance = cls()
        return cls._engine
    
    @classmethod
    def check_connection(cls,self):
        try:
            engine = cls.get_instance(self)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                print('✅ Conexión a la base de datos exitosa.') 
                return True
        except Exception as error:
            logging.error(f"❌ Error de conexión a la base de datos: {error}")
            return False
        
    
    
    
    
