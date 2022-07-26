from fastapi import FastAPI
from routes.routeGeneral import  api
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = ["*"]

app.include_router(api)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)