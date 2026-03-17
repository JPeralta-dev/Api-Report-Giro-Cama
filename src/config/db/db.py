from sqlalchemy import Engine, create_engine, text
from typing import Optional
from src.config.env.env import settings
import logging

class DataBase:
    _engine: Optional[Engine] = None

    @classmethod 
    def get_engine(cls) -> Engine:
        if cls._engine is None:
            connection_string = (
                f"mssql+pyodbc://{settings.DB_USER}:{settings.DB_PASSWORD}"
                f"@{settings.DB_SERVER}/{settings.DB_NAME}"
                f"?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
            )
            ##print(connection_string)
            cls._engine = create_engine(connection_string, pool_size=10, max_overflow=20)
        return cls._engine
    

    @classmethod
    def check_connection(cls) -> bool:
        try:
            with cls.get_engine().connect() as conn:
                conn.execute(text("SELECT 1"))
                logging.info("Conexion a base de datos exitosa")
                return True
        except Exception as error:
            logging.error("Error de conexion a base de datos: %s", error)
            return False