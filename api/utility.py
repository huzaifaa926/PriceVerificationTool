import csv
from thefuzz import fuzz

def load_data():
    data = []
    filename = '../resources/PriceList.csv'
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            temp = {}
            temp['goods_desc'] = row[0]
            temp['uom'] = row[1]
            temp['price'] = row[2]
            temp['currency'] = row[3]
            temp['link'] = row[4]
            data.append(temp)
    return data[1:] # Removes header


# fuzz.ratio
# fuzz.partial_ratio
# fuzz.token_sort_ratio
# fuzz.token_set_ratio

def fuzzy_extract(query, choices, algo, threshold):
    results = []
    for item in choices:
        if algo == "ratio":
            if fuzz.ratio(query, item['goods_desc']) >= threshold:
                results.append(item)
        elif algo == "partial_ratio":
            if fuzz.partial_ratio(query, item['goods_desc']) >= threshold:
                results.append(item)
        elif algo == "token_sort_ratio":
            if fuzz.token_sort_ratio(query, item['goods_desc']) >= threshold:
                results.append(item)
        else:
            if fuzz.token_set_ratio(query, item['goods_desc']) >= threshold:
                results.append(item)
    return results