from typing import Union
from fastapi import FastAPI
import csv

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens if token.isalpha()]
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

def load_data():
    data = []
    filename = '../resources/PriceList.csv'
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            temp = {}
            for column in row:
                temp['hs_code'] = column
                temp['goods_desc'] = column
                temp['uom'] = column
                temp['price'] = column
                temp['currency'] = column
            data.append(temp)
    return data


app = FastAPI()
data = load_data()


@app.get("/")
def read_root():
    return {"message":"Price Verification Tool"}


@app.get("/pvt/api/product_search/{good_desc}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/pvt/api/preprocess/{text}")
def read_item(text: str):
    return {"preprocessed_text": preprocess_text(text)}
