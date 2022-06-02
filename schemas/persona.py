from sqlite3 import Date
from pydantic import BaseModel

class Personas (BaseModel):
    pers_ced: int
    pers_nombre: str
    pers_fecha_nacimiento: Date
    pers_genero: str
    pers_email: str
    pers_direccion: str
    pers_celular: str
    muni_id: int
    depa_id: int