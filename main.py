#API REST: Interfaz de Programacion de aplicaciones para compartir recursos
from typing import List, Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

#Inicializamos un objeto donde tendra las caracteristicas de una API REST
app = FastAPI()

#Definimos el modelo
class Curso(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int

#Simularemos una base de datos
cursos_db = []

#CRUD: Read (lectura) GET ALL: Leeremos todos los cursos que haya en la db
@app.get("/cursos/", response_model=List[Curso])
def obtener_curso():
    return cursos_db

#CRUD: Create (Escribir) POST: Agregraremos un nuevo recurso a nuestra base de datos
@app.post("/cursos/",response_model=Curso)
def crear_curso(curso: Curso):
    curso.id = str(uuid.uuid4()) #Usamos UUID para generar un ID unico e irrepetible
    cursos_db.append(curso)
    return curso

#CRUD: Read (Lectura) GET (individual): Leeremos un curso que coincida con el ID
@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) #Con next obtenemos el primer elemento que coincida con el ID
    if curso is None:
        raise HTTPException(status_code=404,detail="El curso no encontrado")
    return curso

#CRUD: Update (Actualizar/Modificar) PUT: Modificaremos un recurso que coincida con el ID que mandemos
@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id:str, curso_actualizado:Curso):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None)
    if curso is None:
        raise HTTPException(status_code=404,detail="El curso no encontrado")
    curso_actualizado.id = curso.id
    index = cursos_db.index(curso) # Buscamos el indice exacto donde esta el curso en nuestra lista (DB)
    cursos_db[index] = curso_actualizado
    return curso_actualizado   

#CRUD: Delete (Eliminar) DELETE: Eliminaremos un recurso que coincida con el ID que mandemos
@app.delete("/cursos/{curso_id}", response_model=Curso) 
def eliminar_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None)
    if curso is None:
        raise HTTPException(status_code=404,detail="El curso no encontrado")
    cursos_db.remove(curso)
    return curso