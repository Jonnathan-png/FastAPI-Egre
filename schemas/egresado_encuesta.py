from pydantic import BaseModel

class Egresado_encuesta (BaseModel):
    egre_id: int
    pers_ced: int
    egre_inicio: str
    egre_fechafin: str
    egre_laboractual: str
    egre_laborrespue: str
    egre_cargo: str
    egre_entidad: str
    egre_sector: str
    egre_tipocontrato: str
    egre_experiencia: str
    egre_estudio: str
    egre_creadoEmpre: str
    egre_nombreEmpre: str
    egre_finalidadEmpre: str
    egre_Aporte: str
    egre_ApoyoAcred: str