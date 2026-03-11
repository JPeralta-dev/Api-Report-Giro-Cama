import pandas as pd
from sqlalchemy import Engine

query = """SELECT DISTINCT

    ADNCENATE.ACANOMBRE                         AS SEDE,

    H.HSUNOMBRE                                 AS SERVICIO,

    B.HCANOMBRE                                 AS CATEGORIA,

    B.HCACODIGO                                 AS CAMA,

    CACCCANTCAMSER.CANTIDAD_CAMAS_REALES        AS TOTAL_CAMAS_REALES,

    CACCCANTCAMSER.CANTIDAD_OCUPADAS            AS CAMAS_OCUPADAS,

    CACCCANTCAMSER.CANTIDAD_LIBRES              AS CAMAS_LIBRES,

    (SELECT COUNT(*)
     FROM HPNDEFCAM hdc
     WHERE hdc.HCAESTADO = '6'
       AND hdc.ADNCENATE = ADNCENATE.OID
       AND hdc.HPNTIPOCA IN (8))                AS CAMAS_INACTIVAS,

    -- Fechas de ocupación
    A.HESFECING                                 AS INICIO_OCUPACION,

    A.HESFECSAL                                 AS FIN_OCUPACION,

    -- Cálculo de días ocupados
    DATEDIFF(
        DAY,
        A.HESFECING,
        ISNULL(A.HESFECSAL, GETDATE())
    )                                           AS DIAS_OCUPADOS

FROM DGEMPRES01.dbo.HPNDEFCAM AS B

INNER JOIN DGEMPRES01.dbo.HPNSUBGRU  AS H  ON B.HPNSUBGRU  = H.OID
INNER JOIN DGEMPRES01.dbo.GENARESER  AS I  ON H.GENARESER  = I.OID
INNER JOIN DGEMPRES01.dbo.HPNGRUPOS       ON HPNGRUPOS.OID = B.HPNGRUPOS
INNER JOIN DGEMPRES01.dbo.ADNCENATE       ON ADNCENATE.OID = B.ADNCENATE

LEFT JOIN DGEMPRES01.dbo.CACCCANTCAMSER  
       ON H.HSUCODIGO = CACCCANTCAMSER.HSUCODIGO

LEFT JOIN DGEMPRES01.dbo.HPNESTANC AS A  
       ON A.HPNDEFCAM = B.OID

WHERE ADNCENATE.ACANOMBRE = 'ALTA COMPLEJIDAD DEL CARIBE'
  AND B.HPNTIPOCA IN (1,2,3,4)
  AND B.HCAESTADO NOT IN ('6')

  AND (
      A.HESFECING >= '2026-01-01'
      OR A.HESFECSAL >= '2026-01-01'
      OR A.HESFECSAL IS NULL
  )"""
  
  
def get_camas(engine: Engine):
    df = pd.read_sql(query,engine)
    return df.to_dict(orient="records")