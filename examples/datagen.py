"""
Create 2 topics to play with
"""
from confluent_kafka import Producer, Consumer
from random import randint, sample
import json


p = Producer({'bootstrap.servers': 'localhost:9092'})
c = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'sales'
})
c.subscribe(['sales1', 'reviews1'])

companies = ['abc', 'def', 'ghi', 'jkl', 'mno', 'pqr', 'stu', 'vwx', 'yz']
products = [101, 201, 301]
feedback = ["terrible", "bad", "ok", "good", "great"]
stores = [i + str(randint(1, 10)) for i in companies]

while True:
    p.poll(1.0)  # limit production to once per second

    sales = {
        'company_name': sample(companies, 1)[0],
        'product': sample(products, 1)[0],
        'quantity': randint(1000, 100000),
        'store': sample(stores, 1)[0]
    }

    reviews = {
        'company_name': sample(companies, 1)[0],
        'store': sample(stores, 1)[0],
        'product': sample(products, 1)[0],
        'review': sample(feedback, 1)[0]
    }

    p.produce('sales1', json.dumps(sales))
    p.produce('reviews1', json.dumps(reviews))

    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        continue
    print(json.loads(msg.value()))
