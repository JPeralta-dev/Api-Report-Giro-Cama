from fastapi import FastAPI, APIRouter
from src.api.router.route import RouterReports


app =  FastAPI()

app.include_router(RouterReports())
 
@app.get('/ping')
def get_health():
    return { "message":" pong "}