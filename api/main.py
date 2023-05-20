from fastapi import FastAPI
from thefuzz import fuzz, process

from models import SearchQuery
from utility import *





app = FastAPI()

@app.get("/")
def root():
    return {"message" : "Price Verification Tool"}


@app.post("/pvt/api/v1/search")
def search(query: SearchQuery):
    data = load_data()
    # descs = [item["goods_desc"] for item in data]
    # output = process.extractWithoutOrder(query.goods_desc, descs, scorer=fuzz.token_set_ratio, score_cutoff=query.threshold)
    output = fuzzy_extract(query.goods_desc, data, query.algo, query.threshold)
    
    return {"query" : output}

