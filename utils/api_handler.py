# utils/api_handler.py

import requests
import os


def fetch_all_products():
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print("Successfully fetched products from API")
        return response.json().get("products", [])

    except requests.exceptions.RequestException as e:
        print("✗ API fetch failed:", e)
        return []


def create_product_mapping(api_products):
    product_mapping = {}

    for product in api_products:
        product_mapping[product.get('id')] = {
            'category': product.get('category'),
            'brand': product.get('brand'),
            'rating': product.get('rating')
        }

    return product_mapping


def enrich_sales_data(transactions, product_mapping):
    enriched_transactions = []

    for t in transactions:
        enriched = t.copy()

        try:
            numeric_id = int(''.join(filter(str.isdigit, t['ProductID'])))
        except ValueError:
            numeric_id = None

        if numeric_id in product_mapping:
            enriched['API_Category'] = product_mapping[numeric_id]['category']
            enriched['API_Brand'] = product_mapping[numeric_id]['brand']
            enriched['API_Rating'] = product_mapping[numeric_id]['rating']
            enriched['API_Match'] = True
        else:
            enriched['API_Category'] = None
            enriched['API_Brand'] = None
            enriched['API_Rating'] = None
            enriched['API_Match'] = False

        enriched_transactions.append(enriched)

    return enriched_transactions


def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    if not enriched_transactions:
        print("No enriched data to save.")
        return

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    headers = list(enriched_transactions[0].keys())

    with open(filename, 'w', encoding='utf-8') as file:
        file.write("|".join(headers) + "\n")

        for t in enriched_transactions:
            row = [
                str(t.get(h)) if t.get(h) is not None else ""
                for h in headers
            ]
            file.write("|".join(row) + "\n")

    print(f"Enriched data saved to: {filename}")
