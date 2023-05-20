from thefuzz import fuzz, process

s1 = "BALL BEARING"
# s2 = "High Speed Hybrid Ceramic Ball Bearings 6201 6205 608 8*22*7mm Deep Groove Ball Bearing"
s2 = "Ball Ball Bearing Bearing Bearing"


print(fuzz.ratio(s1, s2))
print(fuzz.partial_ratio(s1, s2))
print(fuzz.token_sort_ratio(s1, s2))
print(fuzz.token_set_ratio(s1, s2))



s = ["Mobile Phone", "Cellphone", "Phone", "IPhone", "Samsung"]


print(process.extract("phone", s, scorer=fuzz.token_set_ratio))


# descs = [item["goods_desc"] for item in data]
# output = process.extractWithoutOrder(query.goods_desc, descs, scorer=fuzz.token_set_ratio, score_cutoff=query.threshold)





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
