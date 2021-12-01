import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dr_tart.settings")
django.setup()

from products.models import Product

CSV_PATH_PRODUCTS = "./desktop/test_product.csv"

with open(CSV_PATH_PRODUCTS) as in_file:
	data_reader = csv.reader(in_file)
	next(data_reader, None)
	for row in data_reader:  		
		Product.objects.create(
			korean_name = row[0],
			english_name = row[1],
   			image = row[2],
			price = row[3],
			vegan_or_not = row[4],
			sugar_level = row[5],
			description = row[6],
			category = row[7]
		)

