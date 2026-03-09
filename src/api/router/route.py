from fastapi import APIRouter
from src.config.db.db import DataBase
from src.services.get_query_giro_camas import get_giro_camas
from src.processing.giro_cama import proccesing_query_giro_cama

import pandas as pd

router = APIRouter(prefix="/v1/reports", tags=["Reportes"])

def RouterReports () -> APIRouter:
    
    @router.get("/")
    def get_report_giro_cama():
        engine = DataBase.get_engine()
        return proccesing_query_giro_cama(get_giro_camas(engine))
    

    @router.get("/servicios")
    def get_servicios_giro_cama():
        df = pd.read_excel("C:/Users/juan.peralta/Downloads/DGReporte - COMPORTAMIENTO POR CAMA V2.xlsx")
        for s in sorted(df["SERVICIO"].dropna().unique()):
            print(f'"{s}",')
        return 
    return router


    
