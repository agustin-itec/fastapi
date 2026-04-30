from fastapi import FastAPI, Body, Path, Query

app = FastAPI()

app.title = "Mi primera Api"
app.version = "0.0"


articulos = [
    {"id": 1, "nombre": "Serrucho", "precio": 10000, "activo": True},
    {"id": 2, "nombre": "Martillo", "precio": 5000, "activo": True},
    {"id": 3, "nombre": "Taladro", "precio": 50000,"activo": True },
]


@app.get("/articulos")
async def get_articulos():
    return articulos


@app.get("/articulo/{id}") #obtengo por id
async def get_articulos_id(id:int):
    for articulo in articulos:
        if articulo["id"] == id:
            return articulo
    return {"status": "Not found"}

@app.delete("/articulo/{id}") #obtengo por id
async def delete_articulos_id(id:int = Path(gt=0), logico: bool = Query(description="True si borrado logico"),):
    for articulo in articulos:
        if articulo["id"] == id:
            if logico:
                articulo["activo"] = False
            articulos.remove(articulo)
            return articulos





@app.post("/articulos") #parametro query -> endpoint?clave=valor&otra_clave=valor
async def crear_articulo(id: int = Body(), nombre: str = Body(), precio: int = Body()):
    nuevo_art = {
        "id": id,
        "nombre": nombre,
        "precio": precio
    }
    articulos.append(nuevo_art)


#para int:
#gt greater than
#ge grater or equal
#lt less than
#le less or equal

#para str:
# min_length
# max_length

@app.put("/articulos/{id}")
async def editar_articulo(id: int = Path(gt=0, description="Id del articulo para editar"), nombre: str = Body(max_length=50, min_length=2), precio: int = Body(ge=1000, lt=9900000)):
    for articulo in articulos:
        if articulo["id"] == id:
            articulo["nombre"] = nombre
            articulo["precio"] = precio
            return articulo
    return {"status": "Not found"} 
    

@app.get("/home/{nombre}")
async def home(nombre):
    return {"Hola": nombre}



@app.put("/saludo/put")
async def put():
    return {"Hola":"put"}

@app.post("/saludo/post")
async def post():
    return {"Hola":"post"}


@app.delete("/saludo/delete")
async def delete():
    return {"Hola":"delete"}
