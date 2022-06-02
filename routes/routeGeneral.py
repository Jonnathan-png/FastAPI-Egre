#FASTAPI
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#CONECTION
from database.connectToDatabase import conn
#MODELS
from models.Models import departamento, municipio, persona, usuario, egresado_encuesta
from schemas.egresado_encuesta import Egresado_encuesta
#SCHEMAS
from schemas.persona import Personas
from schemas.user import Users
#HTTP
from http.client import HTTPException
#Criptografia
from passlib.context import CryptContext
#Datetime
from datetime import datetime, timedelta
#JSON WEB TOKEN
from jose import jwt


api = APIRouter()



#--------------------------------------------------------------------------------------------
#USERS
#Cifrado de contraseña

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def get_password_hash(password):
    return pwd_context.hash(password)

#Generacion Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user (username, password):
    user = conn.execute(usuario.select().where(usuario.c.username == username)).all()
    #user = session.query(usuario).from_statement(text("SELECT * FROM usuario where username=:username")).params(username=username).all()
    print(user[0].password)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect User or Password")
    password_check = pwd_context.verify(password, user[0].password)
    if password_check:
        return password_check
    else:
        return False  
    print(password_check)           

SECRET_KEY = 'c0128cb54ca05ea505448d39c295526cb5d74c3abdedfe2efa80c9fd77a5d2c4'
ALGORITHM = 'HS256'

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(encoded_jwt)

    return encoded_jwt

@api.post("/token",tags=["Users"])
def login (form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    if authenticate_user(username,password):
        access_token = create_access_token(
            data = {"sub": username}, expires_delta = timedelta(minutes=30)
        )
        return {"access_token": access_token, "token_type": "bearer" , "username": username}
    else:
        raise HTTPException(status_code=400, detail="Incorrect User or Password")

@api.get("/",tags=["Users"])
def mifuncion(token: str = Depends(oauth2_scheme)):
    return {"token": token}
    
@api.get("/getUsers", tags=["User"])
def getUsers(token: str = Depends(oauth2_scheme)):
    return conn.execute(usuario.select()).fetchall()
    #return session.query(usuario).from_statement(text("SELECT * FROM usuario")).all()


@api.post('/creatUser',  tags=["User"])
async def creatUser(user: Users):
    new_user = {"username": user.username, 
                "password": get_password_hash(user.password)}

    result = conn.execute(usuario.insert().values(new_user))

    return {"message":"Registrado correctamente"}

#DEPARTAMENTO
@api.get("/getDepartamentos", tags=["Departamento"])
def getDepart(token: str = Depends(oauth2_scheme)):
    return conn.execute(departamento.select()).fetchall()

#MUNICIPIO
@api.get("/getMunicipios", tags=["Municipio"])
def getMunicipios(token: str = Depends(oauth2_scheme)):
    return conn.execute(municipio.select()).fetchall()

@api.get(
    '/getMunicipio/{id}', tags=["Municipio"])
async def getMunicipio(depa_id, token: str = Depends(oauth2_scheme)):
    return conn.execute(municipio.select().where(municipio.c.depa_id == depa_id)).all()

#PERSONA
@api.get("/getPersons", tags=["Persona"])
def getPersonas(token: str = Depends(oauth2_scheme)):
    return conn.execute(persona.select()).fetchall()

@api.get('/getPerson/{id}', tags=["Persona"])
async def getPersona(id, token: str = Depends(oauth2_scheme)):
    return conn.execute(persona.select().where(persona.c.pers_ced == id)).first()

@api.get('/getPersonbyDep/{dep_id}', tags=["Persona"])
async def getPersonabyDep(dep_id, token: str = Depends(oauth2_scheme)):
    return conn.execute(persona.select().where(persona.c.depa_id == dep_id)).first()

@api.post('/creatPerson',  tags=["Persona"])
async def creatPerson(person: Personas, token: str = Depends(oauth2_scheme)):
    pers = dict(person)
    result = conn.execute(persona.insert().values(pers))
    return {"message":"Registrado correctamente"}

@api.delete('/delPerson/{id}', tags=["Persona"])
async def delPersona(id, token: str = Depends(oauth2_scheme)):
    result = conn.execute(persona.delete().where(persona.c.pers_ced == id))
    return {"message": "Eliminado correctamente"}

@api.put('/updPerson/{id}', tags=["Persona"])
async def updPerson(id, person:Personas, token: str = Depends(oauth2_scheme)):
    conn.execute(persona.update().
        values(pers_nombre = person.pers_nombre, 
            pers_fecha_nacimiento = person.pers_fecha_nacimiento,
            pers_genero = person.pers_genero,
            pers_email = person.pers_email,
            pers_direccion = person.pers_direccion,
            pers_celular = person.pers_celular,
            muni_id = person.muni_id,
            depa_id = person.depa_id)
            .where(persona.c.pers_ced == id))
    
    return {"message":"Actualizado correctamente"}

#EGRESADO-ENCUESTA
@api.get("/getEgreEncu", tags=["Egresado"])
def getEgresados(token: str = Depends(oauth2_scheme)):
    return conn.execute(egresado_encuesta.select()).fetchall()

@api.get('/getEgreEncu_Ced/{ced}', tags=["Egresado"])
async def getEgreEncu_Ced(ced, token: str = Depends(oauth2_scheme)):
    return conn.execute(egresado_encuesta.select().where(egresado_encuesta.c.pers_ced == ced)).first()

@api.get('/getEgreEncu_Inic/{egre_inicio}', tags=["Egresado"])
async def getEgreEncu_Inic(egre_inicio, token: str = Depends(oauth2_scheme)):
    return conn.execute(egresado_encuesta.select().where(egresado_encuesta.c.egre_inicio == egre_inicio)).first()

@api.get('/getEgreEncu_Apo/{egre_ApoyoAcred}', tags=["Egresado"])
async def getEgreEncu_Apo(egre_ApoyoAcred, token: str = Depends(oauth2_scheme)):
    return conn.execute(egresado_encuesta.select().where(egresado_encuesta.c.egre_ApoyoAcred == egre_ApoyoAcred)).first()

@api.post('/createEgreEnc',  tags=["Egresado"])
async def createEgreEnc(egreenc: Egresado_encuesta, token: str = Depends(oauth2_scheme)):
    pers = dict(egreenc)
    result = conn.execute(egresado_encuesta.insert().values(pers))
    return {"message":"Registrado correctamente"}

@api.delete('/delEgreEnc/{id}', tags=["Egresado"])
async def delEgreEnc(id, token: str = Depends(oauth2_scheme)):
    result = conn.execute(egresado_encuesta.delete().where(egresado_encuesta.c.egre_id == id))
    return {"message": "Eliminado correctamente"}

@api.put('/updEgreEnc/{id}', tags=["Egresado"])
async def updEgreEnc(id, egreenc: Egresado_encuesta, token: str = Depends(oauth2_scheme)):
    conn.execute(egresado_encuesta.update().
        values(egre_inicio = egreenc.egre_inicio, 
            egre_fechafin = egreenc.egre_fechafin,
            egre_laboractual = egreenc.egre_laboractual,
            egre_laborrespue = egreenc.egre_laborrespue,
            egre_cargo = egreenc.egre_cargo,
            egre_entidad = egreenc.egre_entidad,
            egre_sector = egreenc.egre_sector,
            egre_tipocontrato = egreenc.egre_tipocontrato,
            egre_experiencia = egreenc.egre_experiencia,
            egre_estudio = egreenc.egre_estudio,
            egre_creadoEmpre = egreenc.egre_creadoEmpre,
            egre_nombreEmpre = egreenc.egre_nombreEmpre,
            egre_Aporte = egreenc.egre_Aporte,
            egre_ApoyoAcred = egreenc.egre_ApoyoAcred)
            .where(egresado_encuesta.c.egre_id == id))
    
    return {"message":"Actualizado correctamente"}