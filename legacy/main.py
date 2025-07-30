from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Configuración de BD
DATABASE_URL = "sqlite:///./usuarios.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Modelo ORM
class UsuarioORM(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    email = Column(String)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Modelo Pydantic
class Usuario(BaseModel):
    id: int
    nombre: str
    email: str
    class Config:
        orm_mode = True

app = FastAPI()

# ENDPOINTS

@app.get("/usuarios")
def listar_usuarios():
    db = SessionLocal()
    datos = db.query(UsuarioORM).all()
    db.close()
    return datos

@app.post("/usuarios")
def crear_usuario(usuario: Usuario):
    db = SessionLocal()
    nuevo = UsuarioORM(id=usuario.id, nombre=usuario.nombre, email=usuario.email)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    db.close()
    return nuevo

@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    db = SessionLocal()
    usuario = db.query(UsuarioORM).filter(UsuarioORM.id == usuario_id).first()
    if not usuario:
        db.close()
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(usuario)
    db.commit()
    db.close()
    return {"mensaje": "Eliminado"}
