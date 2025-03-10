from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from pymbtiles import MBtiles

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/vector/{z}/{x}/{y}.pbf")
def vectortile(z: int, x: int, y: int):
    # xyz -> tms
    y = 2**z - y - 1
    with MBtiles("vector.mbtiles") as src:
        tile_data = src.read_tile(z=z, x=x, y=y)
    if tile_data is None:
        return Response(status_code=404)
    
    return Response(
        content=tile_data,
        media_type="application/vnd.mapbox-vector-tile",
        headers={"content-encoding": "gzip"},
    )

    # MBTiles形式のタイルデータはgzip圧縮されているため、content-encodingヘッダーが必要

@app.get("/raster/{z}/{x}/{y}.png")
def rastertile(z: int, x: int, y: int):
    y = 2 ** z - y - 1  # xyz -> tms
    with MBtiles("raster.mbtiles") as src:
        tile_data = src.read_tile(z=z, x=x, y=y)
    if tile_data is None:
        return Response(status_code=404)
    return Response(content=tile_data, media_type="image/png")

app.mount("/", StaticFiles(directory="static"), name="static")