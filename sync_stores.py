import requests
import json
import configparser

# Load the API credentials and URLs for each store from the config file
config = configparser.ConfigParser()
config.read('stores.ini')
stores = config.sections()

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
                    data = {
                        "location_id": 123456789, # replace with the appropriate location ID for the other store
                        "available": inventory
                    }
                    set_inventory_url = f"{other_url}/admin/api/2021-09/products/{product_id}/inventory_levels/set.json"
                    set_inventory_response = requests.post(set_inventory_url, auth=(other_api_key, other_password), json=data)
                else:
                    data = {
                        "location_id": 123456789, # replace with the appropriate location ID for this store
                        "available": other_inventory
                    }
                    set_inventory_url = f"{url}/admin/api/2021-09/products/{product_id}/inventory_levels/set.json"
                    set_inventory_response = requests.post(set_inventory_url, auth=(api_key, password), json=data)
