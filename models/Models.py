from sqlalchemy import ForeignKey, ForeignKeyConstraint, Table, Column
from sqlalchemy.sql.sqltypes import String,Integer,Date
from database.connectToDatabase import meta, engine

departamento = Table("departamento", meta, 
    Column("depa_id",Integer, primary_key=True),
    Column("depa_nombre", String(255)))

municipio = Table("municipio", meta,
    Column("muni_id", Integer, primary_key=True),
    Column("muni_nombre", String(255)),
    Column('depa_id', Integer),
    ForeignKeyConstraint(
        ['depa_id'], ['departamento.depa_id'],
        use_alter=True, name='fk_dep_mun_depmun_id'
    ))

persona = Table("persona", meta,
    Column("pers_ced", Integer, primary_key=True),
    Column("pers_nombre", String(100)),
    Column("pers_fecha_nacimiento", Date),
    Column("pers_genero", String(25)),
    Column("pers_email", String(50)),
    Column("pers_direccion", String(255)),
    Column("pers_celular", String(25)),
    Column("muni_id", Integer),
    Column("depa_id",Integer),
    ForeignKeyConstraint(
        ['muni_id'], ['municipio.muni_id'],
        use_alter=True, name='fk_pers_mun_id'
    ),
    ForeignKeyConstraint(
        ['depa_id'], ['departamento.depa_id'],
        use_alter=True, name='fk_pers_depa_id'
    ))

usuario = Table("usuario", meta, 
    Column("username",Integer, primary_key=True),
    Column("password", String(255)))

egresado_encuesta = Table("egresado_encuesta", meta, 
    Column("egre_id",Integer, primary_key=True),
    Column("pers_ced",Integer),
    Column("egre_inicio", String(50)),
    Column("egre_fechafin", String(15)),
    Column("egre_laboractual", String(20)),
    Column("egre_laborrespue", String(100)),
    Column("egre_cargo", String(50)),
    Column("egre_entidad", String(50)),
    Column("egre_sector", String(20)),
    Column("egre_tipocontrato", String(20)),
    Column("egre_experiencia", String(20)),
    Column("egre_estudio", String(50)),
    Column("egre_creadoEmpre", String(20)),
    Column("egre_nombreEmpre", String(50)),
    Column("egre_Aporte", String(255)),
    Column("egre_ApoyoAcred", String(255)),
    ForeignKeyConstraint(
        ['pers_ced'], ['persona.pers_ced'],
        use_alter=True, name='fk_pers_pers_ced')) 

meta.create_all(engine)