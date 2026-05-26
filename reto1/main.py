#from fastapi import FastAPI, Body, Path, Query
#
#app = FastAPI()
#
#app.title = "Mi primera Api"
#app.version = "0.0"
#
#
#articulos = [
#    {"id": 1, "nombre": "Serrucho", "precio": 10000, "activo": True},
#    {"id": 2, "nombre": "Martillo", "precio": 5000, "activo": True},
#    {"id": 3, "nombre": "Taladro", "precio": 50000,"activo": True },
#]
#
#
#@app.get("/articulos")
#async def get_articulos():
#    return articulos
#
#
#@app.get("/articulo/{id}") #obtengo por id
#async def get_articulos_id(id:int):
#    for articulo in articulos:
#        if articulo["id"] == id:
#            return articulo
#    return {"status": "Not found"}
#
#@app.delete("/articulo/{id}") #obtengo por id
#async def delete_articulos_id(id:int = Path(gt=0), logico: bool = Query(description="True si borrado logico"),):
#    for articulo in articulos:
#        if articulo["id"] == id:
#            if logico:
#                articulo["activo"] = False
#            articulos.remove(articulo)
#            return articulos
#
#
#
#
#
#@app.post("/articulos") #parametro query -> endpoint?clave=valor&otra_clave=valor
#async def crear_articulo(id: int = Body(), nombre: str = Body(), precio: int = Body()):
#    nuevo_art = {
#        "id": id,
#        "nombre": nombre,
#        "precio": precio
#    }
#    articulos.append(nuevo_art)
#
#
#para int:
#gt greater than
#ge grater or equal
#lt less than
#le less or equal
#
#para str:
# min_length
# max_length
#
#@app.put("/articulos/{id}")
#async def editar_articulo(id: int = Path(gt=0, description="Id del articulo para editar"), nombre: str = Body(max_length=50, min_length=2), precio: int = Body(ge=1000, lt=9900000)):
#    for articulo in articulos:
#        if articulo["id"] == id:
#            articulo["nombre"] = nombre
#            articulo["precio"] = precio
#            return articulo
#    return {"status": "Not found"} 
#    
#
#@app.get("/home/{nombre}")
#async def home(nombre):
#    return {"Hola": nombre}
#
#
#
#@app.put("/saludo/put")
#async def put():
#    return {"Hola":"put"}
#
#@app.post("/saludo/post")
#async def post():
#    return {"Hola":"post"}
#
#
#@app.delete("/saludo/delete")
#async def delete():
#    return {"Hola":"delete"}

from typing import Annotated
from pydantic import BaseModel, Field

from fastapi import FastAPI, Body, Path, Query, HTTPException

from fastapi.middleware.cors import CORSMiddleware
#request --> middware --> path operation --> middware --> response




app = FastAPI(title="API práctica", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://127.0.0.1:5500',],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)


productos = [
    {"id": 1, "nombre": "Leña en bolsa", "peso": 6, "precio": 2300, "disponible": True},
    {"id": 2, "nombre": "Leña en bolsa", "peso": 15, "precio": 6000, "disponible": True},
    {"id": 3, "nombre": "Carbón en bolsa", "peso": 3, "precio": 2300, "disponible": True},
]


dict_not_found:dict = {
    404: {
        "description": "Si el artículo no se encuentra en la lista",
        "content": {
            "aplication/json": {
                "example": {
                    "detail": "Articulo no encontrado"
                }
            }
        }
        }
    }

STR_CORTITO = Annotated[str, Field(max_length=40)]
INT_PVP = Annotated[float, Field(gt=200, lt=999999)] #precio venta al publico


#Annotated: es una mejor optimización para fastapi. al usar este, despues del igual se le puede pasar un valor por defecto despues del igual a los parametros.

#pydantic -> Sirve para esquemar o estructurar objetos a traves del BaseModel

#creacion
class ProductoSchema(BaseModel):
    id: int = Field(gt=0)
    nombre: STR_CORTITO
    peso: Annotated[int, Field(gt=0)] = 1
    precio: INT_PVP = 200
    disponible: Annotated[bool, Field(description = "Sigue disponible?")] = True


#actualizacion (sin id para editar. porque no podemos cambiar los id que vienen de la base de datos)

class ProductoUpdateSchema(BaseModel):
    nombre: STR_CORTITO
    peso: int = Field(gt=0)
    precio: INT_PVP
    disponible: bool = Field(description = "Sigue disponible?")



# get:

@app.get("/productos", response_model=list[ProductoSchema])
async def get_productos():
    return productos


@app.get(
        "/productos/{id}",
        responses=dict_not_found,
        response_model=ProductoSchema
        ) 
async def get_productos_id(id: Annotated[int, Path(gt=0, description="El ID debe ser mayor a cero")]):
    for producto in productos:
        if producto["id"] == id:
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")


# delete

@app.delete("/productos/{id}", responses=dict_not_found, response_model=list[ProductoSchema])
async def delete_articulos_id(id:Annotated[int, Path(gt=0, description="El ID debe ser mayor a cero")], logico: Annotated[bool, Query(description="True si borrado logico")] ):
    for producto in productos:
        if producto["id"] == id:
            if logico:
                producto["disponible"] = False
            else:
                productos.remove(producto)
            return productos


# post

# id: int = Body(gt=0, description="El ID debe ser mayor a cero"), nombre: str = Body(max_length=50, min_length=3

@app.post("/productos", response_model=ProductoSchema) 
async def crear_producto(articulo: ProductoSchema):
    productos.append(articulo.model_dump())
    return articulo

# put

@app.put("/productos/{id}", responses=dict_not_found, response_model=ProductoSchema) #Path param == Param ruta
async def editar_producto(
    id: Annotated[int, Path(gt = 0, description="id del art para editar")],
    producto_update: ProductoUpdateSchema,
    ):
    for art in productos:
        if art["id"] == id:
            art["nombre"] = producto_update.nombre
            art["precio"] = producto_update.precio
            art["peso"] = producto_update.peso
            art["disponible"] = producto_update.disponible
            return art
    raise HTTPException(status_code=404, detail="Producto no encontrado") 
