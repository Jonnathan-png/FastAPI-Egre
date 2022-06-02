from sqlalchemy import  create_engine, MetaData
from sqlalchemy.orm import sessionmaker

#engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/dbEgresado")
engine = create_engine("postgresql://eaykvvtbpjgoiy:67d06ed22b2dbc0bb2355fc04fb310c4870c1e20ebffa3f20be6e84873107dea@ec2-3-234-131-8.compute-1.amazonaws.com:5432/d4n9m39t7qvedj")
meta = MetaData()
conn = engine.connect()

