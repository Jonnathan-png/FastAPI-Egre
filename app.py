from fastapi import FastAPI
from routes.routeGeneral import  api


app = FastAPI()

app.include_router(api)
