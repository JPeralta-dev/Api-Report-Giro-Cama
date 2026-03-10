import pandas as pd
from calendar import monthrange
from datetime import datetime


def get_month_range(year: int, month: int) -> tuple[pd.Timestamp, pd.Timestamp]:
    """Retorna el primer y último momento del mes dado."""
    ultimo_dia = monthrange(year, month)[1]
    inicio_mes = pd.Timestamp(year, month, 1, 0, 0, 0)
    fin_mes    = pd.Timestamp(year, month, ultimo_dia, 23, 59, 59)
    return inicio_mes, fin_mes


def calcular_egresos_y_estancia(
    df: pd.DataFrame,
    year: int,
    month: int,
    categoria: str | None = None,
    servicio: str | None = None,
) -> dict:
    """
    Calcula los egresos y días de estancia promedio para un mes dado.

    Reglas:
    ─────────────────────────────────────────────────────────────────
    Un paciente CUENTA como egresado del mes si:
      1. Su FIN cae dentro del mes  →  egreso real
      2. Está activo (FIN es NaT) y su INICIO está dentro o antes del mes  → 
         se considera egresado al último segundo del mes (cierre de corte)

    Los días de estancia se calculan ACOTADOS al mes:
      - inicio efectivo = max(INICIO, inicio_mes)
      - fin efectivo    = FIN real  ó  fin_mes  (para activos)
      - dias            = (fin_efectivo - inicio_efectivo).total_seconds() / 86400
    ─────────────────────────────────────────────────────────────────

    Parámetros
    ----------
    df        : DataFrame ya procesado por proccesing_query_giro_cama
    year      : año del filtro  (ej. 2026)
    month     : mes del filtro  (ej. 2 para febrero)
    categoria : filtro opcional de CATEGORIA  (ej. "UCI")
    servicio  : filtro opcional de SERVICIO   (ej. "2DO PISO UNIDAD DE QUEMADOS")

    Retorna
    -------
    dict con claves: egresos, dias_estancia_promedio, detalle (lista de dicts)
    """

    inicio_mes, fin_mes = get_month_range(year, month)

    df = df.copy()
    df["INICIO"] = pd.to_datetime(df["INICIO"])
    df["FIN"]    = pd.to_datetime(df["FIN"])     # NaT si está activo

    # ── Filtros opcionales ────────────────────────────────────────────────────
    if categoria:
        df = df[df["CATEGORIA"] == categoria]
    if servicio:
        df = df[df["SERVICIO"] == servicio]

    # ── Identificar registros que pertenecen al mes ───────────────────────────
    # Caso 1: egreso real dentro del mes
    egreso_real  = df["FIN"].notna() & (df["FIN"] >= inicio_mes) & (df["FIN"] <= fin_mes)

    # Caso 2: activo (sin FIN) con INICIO ≤ fin_mes  →  estaba en el mes
    activo_en_mes = df["FIN"].isna() & (df["INICIO"] <= fin_mes)

    df_mes = df[egreso_real | activo_en_mes].copy()

    if df_mes.empty:
        return {"egresos": 0, "dias_estancia_promedio": 0.0, "detalle": []}

    # ── Calcular días de estancia acotados al mes ─────────────────────────────
    # Para activos, usar fin_mes como FIN de corte
    df_mes["FIN_EFECTIVO"]    = df_mes["FIN"].fillna(fin_mes)
    df_mes["FIN_EFECTIVO"]    = df_mes["FIN_EFECTIVO"].clip(upper=fin_mes)

    # No contar días anteriores al mes
    df_mes["INICIO_EFECTIVO"] = df_mes["INICIO"].clip(lower=inicio_mes)

    df_mes["DIAS_ESTANCIA"] = (
        (df_mes["FIN_EFECTIVO"] - df_mes["INICIO_EFECTIVO"])
        .dt.total_seconds() / 86400
    ).clip(lower=0)

    # ── Agrupar por paciente+ingreso (un egreso por ingreso) ──────────────────
    # Sumar días de todos los servicios de ese ingreso dentro del mes
    por_ingreso = (
        df_mes
        .groupby(["IDENTIFICACION", "INGRESO"], as_index=False)
        .agg(
            PACIENTE       = ("PACIENTE",        "first"),
            SEDE           = ("SEDE",             "first"),
            DIAS_ESTANCIA  = ("DIAS_ESTANCIA",    "sum"),
            INICIO_MES     = ("INICIO_EFECTIVO",  "min"),
            FIN_MES        = ("FIN_EFECTIVO",     "max"),
            ACTIVO         = ("FIN",              lambda s: s.isna().any()),
        )
    )

    egresos              = len(por_ingreso)
    dias_estancia_prom   = round(por_ingreso["DIAS_ESTANCIA"].mean(), 1)

    return {
        "egresos":                 egresos,
        "dias_estancia_promedio":  dias_estancia_prom,
        "detalle":                 por_ingreso.to_dict(orient="records"),
    }