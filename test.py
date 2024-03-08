from wcapi import wcapi
from pprint import pprint

sku = input('Ingresa sku producto:')
p = wcapi.get('products', params={'sku': sku}).json()

for i in p:
    pprint(str(i['name'])+' '+ str(i['stock_quantity']))