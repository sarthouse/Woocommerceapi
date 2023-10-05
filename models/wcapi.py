from woocommerce import API
import pandas as pd

wcapi = API(
    url="https://vagner.ar",
    consumer_key='ck_18ae89cd06ed6a9478780f2c66dc0e01a215df11',
    consumer_secret='cs_03bf6d307664c9cf20e5d55a617f4718962c7a09',
    wp_api=True,
    version='wc/v3'
)

def get_products():
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
    print(df)
    df.to_csv('stock.csv', index=False)

