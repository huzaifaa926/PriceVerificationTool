from typing import Union
from fastapi import FastAPI
import csv

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def similarity(text):
    # Load a pre-trained sentence transformer model
    model = SentenceTransformer('distilbert-base-nli-mean-tokens')

    # List of sentences in your database
    sentences = ['This is the first sentence.',
                'This is the second sentence.',
                'This is the third sentence.']

    # User-entered text
    user_text = text

    # Encode the sentences and user text into vectors
    sentence_embeddings = model.encode(sentences)
    user_embedding = model.encode([user_text])

    # Calculate the cosine similarity between user embedding and sentence embeddings
    similarities = cosine_similarity(user_embedding, sentence_embeddings)[0]

    # Threshold for similarity
    similarity_threshold = 0.85

    # Filter out sentences with similarity above the threshold
    similar_sentences = [sentence for sentence, similarity in zip(sentences, similarities) if similarity >= similarity_threshold]

    # Print the similar sentences
    print(f"Similar sentences (>= {similarity_threshold * 100}% similarity):")
    for sentence in similar_sentences:
        print(sentence)



def calculate_tfid(preprocessed_text):
    # List of preprocessed texts
    texts = [preprocessed_text]

    # Initialize TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the texts to obtain TF-IDF features
    features = vectorizer.fit_transform(texts)

    # Get the feature names
    feature_names = vectorizer.get_feature_names()

    # Print the TF-IDF features
    for i, text in enumerate(texts):
        print(f"Features for '{text}':")
        for j, feature in enumerate(feature_names):
            tfidf_value = features[i, j]
            if tfidf_value > 0:
                print(f"- {feature}: {tfidf_value:.4f}")


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


@app.get("/pvt/api/tfid/{preprocessed_text}")
def read_item(preprocessed_text: str):
    return {"tdif": similarity(preprocessed_text)}
