from fastapi import APIRouter
from src.config.db.db import DataBase
from src.services.get_query_giro_camas import get_giro_camas
from src.processing.giro_cama import proccesing_query_giro_cama

router = APIRouter(prefix="/v1/reports", tags=["Reportes"])

def RouterReports () -> APIRouter:
    
    @router.get("/")
    def get_report_giro_cama():
        engine = DataBase.get_engine()
        return proccesing_query_giro_cama(get_giro_camas(engine))
    return router



    
