from fastapi import FastAPI
from routes.routeGeneral import  api
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(api)
app.add_middleware(
        CORSMiddleware,
        allow_origins=['*']
    )
