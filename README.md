#   IDENTIFICACION | INGRESO | SERVICIO | CAMA  | INICIO              | FIN
    123            | 1       | UCI      | A101  | 06/03/2026 08:00    | 06/03/2026 10:00   ← se elimina
    123            | 1       | UCI      | A102  | 06/03/2026 10:00    | 06/03/2026 14:00   ← se elimina
    123            | 1       | UCI      | A103  | 06/03/2026 14:00    | 06/03/2026 18:00   ← se elimina
    123            | 1       | CIRUGÍA  | B201  | 06/03/2026 18:00    | 06/03/2026 20:00   ← real
    123            | 1       | UCI      | A101  | 06/03/2026 20:00    | 07/03/2026 08:00   ← real (volvió)

# Resultado esperado:
    123            | 1       | UCI      | ---   | 06/03/2026 08:00    | 06/03/2026 18:00   ← colapsado
    123            | 1       | CIRUGÍA  | B201  | 06/03/2026 18:00    | 06/03/2026 20:00   ← intacto
    123            | 1       | UCI      | ---   | 06/03/2026 20:00    | 07/03/2026 08:00   ← intacto (es otra estadía)

    pip install pyodbc

## Despliegue con PM2

Este repositorio incluye `ecosystem.config.js` para ejecutar la API con PM2 en producción.

### 1) Preparar entorno

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> Asegúrate de crear un archivo `.env` con las variables de base de datos (`DB_DRIVER`, `DB_SERVER`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`) y de aplicación (`APP_ENV`, `APP_PORT`).

### 2) Levantar con PM2

```bash
pm2 start ecosystem.config.js --env production
pm2 status
```

### 3) Persistir procesos tras reinicio

```bash
pm2 save
pm2 startup
```

### 4) Logs y reinicios

```bash
pm2 logs api-report-giro-cama
pm2 restart api-report-giro-cama
```   