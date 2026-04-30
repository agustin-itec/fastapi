from fastapi import FastAPI, Body, Path, Query

app = FastAPI() 

productos = [
    {"id": 1, "nombre": "Leña en bolsa", "peso (kg)": 6, "precio": 2300, "disponible": True},
    {"id": 2, "nombre": "Leña en bolsa", "peso (kg)": 15, "precio": 6000, "disponible": True},
    {"id": 3, "nombre": "Carbón en bolsa", "peso (kg)": 3, "precio": 2300, "disponible": True},
]


# get:

@app.get("/productos")
async def get_productos():
    return productos


@app.get("/productos/{id}") 
async def get_productos_id(id: int = Path(gt=0, description="El ID debe ser mayor a cero")):
    for producto in productos:
        if producto["id"] == id:
            return producto
    return {"status": "Not found"}


# delete

@app.delete("/productos/{id}")
async def delete_articulos_id(id:int = Path(gt=0, description="El ID debe ser mayor a cero"), logico: bool = Query(description="True si borrado logico"),):
    for producto in productos:
        if producto["id"] == id:
            if logico:
                producto["disponible"] = False
            else:
                productos.remove(producto)
            return productos


# post

@app.post("/productos") 
async def crear_producto(id: int = Body(gt=0, description="El ID debe ser mayor a cero"), nombre: str = Body(max_length=50, min_length=3), precio: int = Body(ge=300, lt=9900000), peso: int = Body(gt=0), disponible: bool = Body()):
    nuevo_producto = {
        "id": id,
        "nombre": nombre,
        "precio": precio,
        "peso (kg)": peso,
        "disponible": disponible
    }
    productos.append(nuevo_producto)
    return nuevo_producto

# put

@app.put("/productos/{id}")
async def editar_producto(id: int = Path(gt=0, description="El ID debe ser mayor a cero"), nombre: str = Body(max_length=50, min_length=2), precio: int = Body(ge=300, lt=9900000), peso: int = Body(gt=0), disponible: bool = Body() ):
    for producto in productos:
        if producto["id"] == id:
            producto["nombre"] = nombre
            producto["precio"] = precio
            producto["peso (kg)"] = peso
            producto["disponible"] = disponible
            return producto
    return {"status": "Not found"} 
    