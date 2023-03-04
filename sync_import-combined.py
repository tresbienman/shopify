import requests
import json
import configparser
import argparse

# Load the API credentials and URLs for each store from the config file
config = configparser.ConfigParser()
config.read('stores.ini')
stores = config.sections()

# Parse command line arguments for import source and target stores
parser = argparse.ArgumentParser()
parser.add_argument('--import_source', help='The store to import products from')
parser.add_argument('--import_target', help='The store to import products to')
args = parser.parse_args()

# If import_source and import_target are specified, import all products from the source store to the target store
if args.import_source and args.import_target:
    source_api_key = config[args.import_source]['api_key']
    source_password = config[args.import_source]['password']
    source_url = config[args.import_source]['url']
    source_products_url = f'{source_url}/admin/api/2021-09/products.json'
    source_products_response = requests.get(source_products_url, auth=(source_api_key, source_password))
    source_products = json.loads(source_products_response.text)['products']
    
    target_api_key = config[args.import_target]['api_key']
    target_password = config[args.import_target]['password']
    target_url = config[args.import_target]['url']
    
    for product in source_products:
        product['id'] = None
        product['published'] = False
        create_product_url = f"{target_url}/admin/api/2021-09/products.json"
        create_product_response = requests.post(create_product_url, auth=(target_api_key, target_password), json={'product': product})
        print(f"Created product {product['title']} in store {args.import_target}")

# If import_source and import_target are not specified, sync inventory levels between all stores
else:
    # Loop through each store and get its products
    for store in stores:
        api_key = config[store]['api_key']
        password = config[store]['password']
        url = config[store]['url']
        products_url = f'{url}/admin/api/2021-09/products.json'
        products_response = requests.get(products_url, auth=(api_key, password))
        products = json.loads(products_response.text)['products']
        
        # Loop through each product and update its inventory levels in all other stores
        for product in products:
            product_id = product['id']
            inventory_url = f"{url}/admin/api/2021-09/products/{product_id}/inventory_levels.json"
            inventory_response = requests.get(inventory_url, auth=(api_key, password))
            inventory = json.loads(inventory_response.text)['inventory_levels'][0]['available']
            
            # Loop through all other stores and update their inventory levels for this product
            for other_store in stores:
                if other_store != store:
                    other_api_key = config[other_store]['api_key']
                    other_password = config[other_store]['password']
                    other_url = config[other_store]['url']
                    other_inventory_url = f"{other_url}/admin/api/2021-09/products/{product_id}/inventory_levels.json"
                    other_inventory_response = requests.get(other_inventory_url, auth=(other_api_key, other_password))
                    other_inventory = json.loads(other_inventory_response.text)['inventory_levels'][0]['available']
                    
                    # Update the inventory level in the other store to match the lowest value between the two stores
                    if inventory < other_inventory:
                        data = {"location_id": 123456789, "available": inventory}
                        requests.post(other_inventory_url, auth=(other_api_key, other_password), json=data)
                    elif inventory > other_inventory:
                        data = {"location_id": 123456789, "available": other_inventory}
                        requests.post(other_inventory_url, auth=(other_api_key, other_password), json=data)
                    else:
                        pass
                    print(f"Updated inventory levels for product {product['title']} between {store} and {other_store}")
                    
                    # Also update the inventory level in the original store to match the lowest value between the two stores
                    if inventory < other_inventory:
                        data = {"location_id": 123456789, "available": inventory}
                        requests.post(inventory_url, auth=(api_key, password), json=data)
                    elif inventory > other_inventory:
                        data = {"location_id": 123456789, "available": other_inventory}
                        requests.post(inventory_url, auth=(api_key, password), json=data)
                    else:
                        pass
                    print(f"Updated inventory levels for product {product['title']} between {store} and {other_store}")

