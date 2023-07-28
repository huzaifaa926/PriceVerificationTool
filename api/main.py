from fastapi import FastAPI
from thefuzz import fuzz, process

from models import SearchQuery
from utility import *
from scrap_alibaba_selenium import *
from fastapi.middleware.cors import CORSMiddleware

from config import *
logging.basicConfig(filename='../logs/app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d %b, %Y %H:%M:%S', level=LOG_LEVEL)


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Price Verification Tool"}


@app.post("/pvt/api/v1/search")
def search(query: SearchQuery):
    logging.info(f"{'-'*10} /pvt/api/v1/search {'-'*10}")
    goods_data = load_goods_data()
    currency_rate = get_currency_rate()
    output = fuzzy_extract(goods_data, currency_rate, query.goods_desc, query.price,
                           query.uom, query.currency, query.algo, query.threshold)
    return {"output": output}


@app.post("/pvt/api/v2/search")
def search(query: SearchQuery):
    logging.info(f"{'-'*10} /pvt/api/v2/search {'-'*10}")
    product_data = scrap(query.goods_desc)
    currency_rate = get_currency_rate()
    output = fuzzy_extract(product_data, currency_rate, query.goods_desc, query.price,
                           query.uom, query.currency, query.algo, query.threshold)
    return {"output": output}


@app.post("/pvt/api/v3/search")
def search(query: SearchQuery):
    logging.info(f"{'-'*10} /pvt/api/v3/search {'-'*10}")
    if already_scrapped(query.goods_desc):
        product_data = load_scrapped_data()
    else:
        product_data = scrap(query.goods_desc)
        store_output(query.goods_desc, product_data)
    currency_rate = get_currency_rate()
    output = fuzzy_extract(product_data, currency_rate, query.goods_desc, query.price,
                           query.uom, query.currency, query.algo, query.threshold)
    return {"output": output}