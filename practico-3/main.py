from typing import Annotated
from pydantic import BaseModel, Field

from fastapi import FastAPI, Body, Path, Query, HTTPException

app = FastAPI(title="API práctico 3", version="1.0")

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

class ProductoSchema(BaseModel):
    id: int = Field(gt=0)
    nombre: STR_CORTITO
    peso: Annotated[int, Field(gt=0)] = 1
    precio: INT_PVP = 200
    disponible: Annotated[bool, Field(description = "Sigue disponible?")] = True

class ProductoUpdateSchema(BaseModel):
    nombre: STR_CORTITO
    peso: int = Field(gt=0)
    precio: INT_PVP
    disponible: bool = Field(description = "Sigue disponible?")

# get:

@app.get("/productos", response_model=list[ProductoSchema])
async def get_productos():
    productos_disponibles = []
    for producto in productos:
        if producto["disponible"]:
            productos_disponibles.append(producto)
    return productos_disponibles

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

@app.post("/productos", response_model=ProductoSchema) 
async def crear_producto(articulo: ProductoSchema):
    productos.append(articulo.model_dump())
    return articulo

# put

@app.put("/productos/{id}", responses=dict_not_found, response_model=ProductoSchema) 
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
    