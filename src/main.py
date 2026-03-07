from fastapi import FastAPI
from src.api.router.route import RouterReports
from src.config.db.db import DataBase

app =  FastAPI()
DataBase.check_connection()

app.include_router(RouterReports())
 
@app.get('/ping')
def get_health():
    return { "message":" pong "}