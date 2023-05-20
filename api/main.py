from fastapi import FastAPI
from thefuzz import fuzz, process

from models import SearchQuery
from utility import *


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Price Verification Tool"}


@app.post("/pvt/api/v1/search")
def search(query: SearchQuery):
    goods_data = load_goods_data()
    currency_rate = get_currency_rate()
    output = fuzzy_extract(goods_data, currency_rate, query.goods_desc, query.price,
                           query.uom, query.currency, query.algo, query.threshold)
    return {"output": output}
