import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError, ConnectionError
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

es = None  # Global placeholder
INDEX_NAME = "cities"

class City(BaseModel):
    name: str
    population: int

@app.on_event("startup")
def startup_event():
    import time
    global es
    es_host = os.getenv("ELASTICSEARCH_HOST", "http://localhost:9200")
    print(f"🔌 Connecting to Elasticsearch at: {es_host}")
    es = Elasticsearch(es_host)

    max_retries = 90
    for attempt in range(max_retries):
        try:
            if es.ping():
                print("✅ Connected to Elasticsearch.")
                break
        except Exception as e:
            print(f"❌ Attempt {attempt+1}/{max_retries}: Elasticsearch not ready: {repr(e)}")
        time.sleep(2)
    else:
        raise RuntimeError("Failed to connect to Elasticsearch after waiting.")

    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME)
        print("📁 Created index:", INDEX_NAME)

@app.get("/health")
def health():
    return {"status": "OK"}

@app.post("/city")
def upsert_city(city: City):
    doc = {"name": city.name, "population": city.population}
    es.index(index=INDEX_NAME, id=city.name.lower(), document=doc)
    return {"message": f"City '{city.name}' added/updated successfully."}

@app.get("/city/{name}")
def get_city_population(name: str):
    try:
        result = es.get(index=INDEX_NAME, id=name.lower())
        return {"city": name, "population": result["_source"]["population"]}
    except NotFoundError:
        raise HTTPException(status_code=404, detail="City not found")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
def read_root():
    return FileResponse("static/index.html")
