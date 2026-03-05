from fastapi import FastAPI


app =  FastAPI()

app.get("/reports")
def get_report_giro_cama():
    return {
        
    }
    
@app.get('/ping')
def get_health():
    return { "message":" pong "}