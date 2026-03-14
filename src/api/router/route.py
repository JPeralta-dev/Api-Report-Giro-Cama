from fastapi import APIRouter, Query
from src.config.db.db import DataBase
from src.services.get_query_giro_camas import get_giro_camas
from src.processing.giro_cama import proccesing_query_giro_cama
from src.processing.metricas_giro_cama import calcular_egresos_y_estancia
from src.services.get_query_camas import get_camas


import pandas as pd

router = APIRouter(prefix="/v1/reports", tags=["Reportes"])

def RouterReports () -> APIRouter:
    
    @router.get("/")
    def get_report_giro_cama():
        engine = DataBase.get_engine()
        df_final = proccesing_query_giro_cama(get_giro_camas(engine))
        return df_final.to_dict(orient="records")
    
    @router.get("/camas")
    def get_report_camas():
        engine = DataBase.get_engine()
        return get_camas(engine)
    
    @router.get("/metricas")
    def get_metricas(
        year:      int         = Query(..., description="Año del filtro, ej: 2026"),
        month:     int         = Query(..., ge=1, le=12, description="Mes del filtro (1-12)"),
        categoria: str | None  = Query(None, description="Filtro por categoría, ej: UCI"),
        servicio:  str | None  = Query(None, description="Filtro por servicio específico"),
    ):
        """
        Retorna egresos y días de estancia promedio para el mes indicado.

        - Incluye pacientes con egreso real (FIN dentro del mes).
        - Incluye pacientes activos (sin FIN) presentes durante el mes;
          su corte se toma en el último segundo del mes.
        """
        engine    = DataBase.get_engine()
        df_raw    = get_giro_camas(engine)
        df        = pd.DataFrame(proccesing_query_giro_cama(df_raw))
        
        return calcular_egresos_y_estancia(
            df        = df,
            year      = year,
            month     = month,
            categoria = categoria,
            servicio  = servicio,
        )
    

    @router.get("/servicios")
    def get_servicios_giro_cama():
        df = pd.read_excel("C:/Users/juan.peralta/Downloads/DGReporte - COMPORTAMIENTO POR CAMA V2.xlsx")
        for s in sorted(df["SERVICIO"].dropna().unique()):
            print(f'"{s}",')
        return 
    return router


    
