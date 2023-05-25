import csv
from thefuzz import fuzz
import os
from datetime import date


def load_goods_data():
    data = []
    filename = '../resources/PriceList.csv'
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        for row in csv_reader:
            temp = {}
            temp['title'] = row[0]
            temp['uom'] = row[1]
            temp['price'] = row[2]
            temp['currency'] = row[3]
            temp['link'] = row[4]
            data.append(temp)
    return data


def load_scrapped_data():
    data = []
    filename = '../resources/ScrappedData.csv'
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        for row in csv_reader:
            temp = {}
            temp['title'] = row[0]
            temp['price'] = row[1]
            temp['currency'] = row[2]
            temp['uom'] = row[3]
            temp['link'] = row[4]
            data.append(temp)
    return data


def get_currency_rate():
    data = {}
    filename = '../resources/CurrencyConversionList.csv'
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        for row in csv_reader:
            data[row[0]] = float(row[1])
    return data


def store_output(query, product_data):
    header = ['title', 'price', 'currency',
              'uom', 'link', 'query', 'date']

    file_exists = os.path.exists('../resources/ScrappedData.csv')
    with open('../resources/ScrappedData.csv', mode='a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(header)
        for product in product_data:
            writer.writerow([product['title'], product['price'], product['currency'],
                             product['uom'], product['link'],
                             query, date.today().strftime("%Y-%m-%d")])


def already_scrapped(query):
    if not os.path.exists('../resources/ScrappedData.csv'):
        return False
    with open('../resources/ScrappedData.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if fuzz.token_set_ratio(query, row[5]) >= 85:
                return True
    return False


def calculate_over_under(currency_rate, org_price, org_currency, price, currency):
    if org_currency != currency:
        price = currency_rate[currency] * price

    if org_price <= price:
        return "Under"
    else:
        return "Over"


# fuzz.ratio
# fuzz.partial_ratio
# fuzz.token_sort_ratio
# fuzz.token_set_ratio

def fuzzy_extract(choices, currency_rate, query, price, uom, currency, algo, threshold):
    results = []
    for item in choices:
        if algo == "ratio":
            if fuzz.ratio(query, item['title']) >= threshold:
                item["Over/Under"] = calculate_over_under(
                    currency_rate, price, currency, float(item["price"]), item["currency"])
                results.append(item)
        elif algo == "partial_ratio":
            if fuzz.partial_ratio(query, item['title']) >= threshold:
                item["Over/Under"] = calculate_over_under(
                    currency_rate, price, currency, float(item["price"]), item["currency"])
                results.append(item)
        elif algo == "token_sort_ratio":
            if fuzz.token_sort_ratio(query, item['title']) >= threshold:
                item["Over/Under"] = calculate_over_under(
                    currency_rate, price, currency, float(item["price"]), item["currency"])
                results.append(item)
        else:
            if fuzz.token_set_ratio(query, item['title']) >= threshold:
                item["Over/Under"] = calculate_over_under(
                    currency_rate, price, currency, float(item["price"]), item["currency"])
                results.append(item)

    return results
