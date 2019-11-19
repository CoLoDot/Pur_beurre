import json
import requests
from sentry_sdk import capture_message, capture_event
from substitut.models import Products


def update():
    capture_message('Start Cron Job')
    products = Products.objects.all()
    nutriscore_number = {1: 'a',
                         2: 'b',
                         3: 'c',
                         4: 'd',
                         5: 'e'}

    for product in products:
        request_update = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&search_terms="
                                      + str(product.name) + "&sort_by=unique_scans_n&page_size=20&json=1")
        response = json.loads(request_update.text)
        capture_event(response)
        products_created = 0
        for product_index in range(0, int(response['count'])):
            if response['products'][product_index]['states_hierarchy'][1] == 'en:complete':
                try:
                    get_name = response['products'][product_index]['product_name']
                except KeyError:
                    get_name = ''
                try:
                    get_url = response['products'][product_index]['url']
                except KeyError:
                    get_url = ''
                try:
                    get_img = response['products'][product_index]['image_front_url']
                except KeyError:
                    get_img = ''
                try:
                    get_nutriscore = response['products'][product_index]['nutrition_grades']
                    for key, value in nutriscore_number.items():
                        if get_nutriscore == value:
                            get_nutriscore = key
                except KeyError:
                    get_nutriscore = ''
                try:
                    categories_tags = response['products'][product_index]['categories_hierarchy'][:]
                    listing_categories = []
                    for c in categories_tags:
                        cleaned_cat = c.split(':')
                        listing_categories.append(cleaned_cat[1])
                    get_cat = listing_categories
                except KeyError:
                    get_cat = ''

                Products.objects.create(name=get_name,
                                        nutriscore=get_nutriscore,
                                        category=get_cat,
                                        picture=get_img,
                                        url=get_url)

                products_created += 1
                if products_created < 100:
                    break