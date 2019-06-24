"""
Create 2 topics
"""
from confluent_kafka import Producer, Consumer
from random import randint, sample
import json


p = Producer({'bootstrap.servers': 'localhost:9092'})
cs = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'sales'
})

cr = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'reviews'
})

companies = ['abc', 'def', 'ghi', 'jkl', 'mno', 'pqr', 'stu', 'vwx', 'yz']
products = [101, 201, 301]
feedback = ["terrible", "bad", "ok", "good", "great"]

while True:
    p.poll(1.0)  # limit production to once per second

    sales = {
        'company_name': sample(companies, 1)[0],
        'product': sample(products, 1)[0],
        'quantity': randint(1000, 100000)
    }
    reviews = {
        'company_name': sample(companies, 1)[0],
        'product': sample(products, 1)[0],
        'review': sample(feedback, 1)[0]
    }

    p.produce('sales', json.dumps(sales))
    p.produce('reviews', json.dumps(reviews))

    s_msg = cs.poll(1.0)
    r_msg = cr.poll(1.0)

    if s_msg is None or r_msg is None:
        continue
    if s_msg.error() or r_msg.error():
        continue


