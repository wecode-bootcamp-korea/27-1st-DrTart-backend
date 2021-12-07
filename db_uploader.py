import os
import django
import csv 

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dr_tart.settings")
django.setup()

from orders.models     import Cart, OrderItem, Order, OrderStatus
from products.models   import Menu, Product, Category, Image, ReviewComment, Review, Menu
from users.models      import User

# CSV_PATH_USERS = './csv/users.csv'

# with open(CSV_PATH_USERS) as in_file:
#     data_reader = csv.reader(in_file)
#     next(data_reader, None)
#     for row in data_reader:
#         User.objects.create(
#             name = row[0], 
#             email = row[1], 
#             password = row[2], 
#             address = row[3],
#             vegan_or_not = row[4]
#             )

CSV_PATH_PRODUCTS = "./csv/products.csv"

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader: 
        if not Menu.objects.filter(name=row[8]).exists():
            Menu.objects.create(
				name = row[8]
		)

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader: 
        if not Category.objects.filter(name=row[7]).exists():
            Category.objects.create(
				name = row[7],
                menu = Menu.objects.get(name=row[8])
		)
            

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if not Product.objects.filter(korean_name=row[0]).exists():  		
            Product.objects.create(
                korean_name = row[0],
                english_name = row[1],
                thumbnail_image_url = row[2],
                price = row[3],
                vegan_or_not = row[4],
                sugar_level = row[5],
                description = row[6],
                category  = Category.objects.get(name = row[7])
		)
  
CSV_PATH_PRODUCTS = "./csv/carts.csv"

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Cart.objects.create(
			quantity = row[0],
            product = Product.objects.get(korean_name=row[1]),
            user = User.objects.get(name=row[2])
        )         
            
CSV_PATH_PRODUCTS = "./csv/images.csv"

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Image.objects.create(
			url = row[0],
            product = Product.objects.get(korean_name=row[1])
        )
        
CSV_PATH_PRODUCTS = "./csv/orders.csv"
 
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if not OrderStatus.objects.filter(status=row[1]).exists():  
            OrderStatus.objects.create(
                status = row[1],
        )  
        
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Order.objects.create(
			address = row[0],
            order_status = OrderStatus.objects.get(status = row[1]),
            user = User.objects.get(name=row[2])
        )        
        
CSV_PATH_PRODUCTS = "./csv/order_items.csv"

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        OrderItem.objects.create(
			quantity = row[0],
            order = Order.objects.get(id=row[1]),
            product = Product.objects.get(korean_name=row[2]),
        )


CSV_PATH_PRODUCTS = "./csv/reviews.csv"

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Review.objects.create(
			content = row[0],
            product = Product.objects.get(korean_name=row[1]),
            user = User.objects.get(name=row[2]),
            review_image_url = row[3]
        )
  
CSV_PATH_PRODUCTS = "./csv/review_comments.csv"

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        ReviewComment.objects.create(
			content = row[0],
            review = Review.objects.get(id=row[1]),
            user = User.objects.get(name=row[2])
        )
        