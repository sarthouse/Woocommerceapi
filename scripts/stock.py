import pandas as pd
from wcapi import wcapi

products = wcapi.get("products", params={'type': 'variable'}).json()
data = []

for product in products:
    product_id = product['id']
    product_name = product['name']
    variations = wcapi.get(f"products/{product_id}/variations").json()
    for variation in variations:
        attributes = variation['attributes']
        variation_name = next(
            (attr['option'] for attr in attributes if attr['name'] == 'Talle' or attr['name'] == 'Talles'), None)
        data.append({
            'Variation ID': variation['id'],
            'SKU': variation['sku'],
            'Product Name': product_name + " " + str(variation_name),
            'Quantity': variation['stock_quantity']
        })

df = pd.DataFrame(data)

df.to_csv('./files/stock.csv', index=False)
