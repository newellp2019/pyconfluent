import json
from pyconfluent.ksql import KSQL
from confluent_kafka import Consumer
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer

"""
process: create 2 streams from existing topics --> JOIN them into another stream --> put the new stream into MySQL table
"""
k = KSQL()

# create the 2 streams (topics created by ../datagen.py), these streams don't really do anything by themselves
sales_stream = k.ksql("CREATE STREAM sales_stream (company_name VARCHAR, product BIGINT, quantity BIGINT, "
                      "store VARCHAR) WITH (KAFKA_TOPIC='sales', VALUE_FORMAT='JSON');")
reviews_stream = k.ksql("CREATE STREAM reviews_stream (company_name VARCHAR, product BIGINT, review VARCHAR, "
                        "store VARCHAR) WITH (KAFKA_TOPIC='reviews', VALUE_FORMAT='JSON');")

# JOIN the two to create an enriched stream (streams created from other streams are very useful
# and run until explicitly terminated)
sales_reviews_stream = k.ksql("CREATE STREAM sales_reviews_stream AS SELECT "
                              "s.company_name, s.product, s.quantity, s.store, "
                              "review FROM sales_stream s "
                              "INNER JOIN reviews_stream r WITHIN 1 SECONDS "
                              "ON s.product = r.product; ")

# connect to the database and create the table
engine = create_engine("mysql+pymysql://peter:password@localhost:3306/vfctest")
meta = MetaData(engine)
sales_reviews = Table("sales_reviews", meta,
                      Column('id', Integer, primary_key=True),
                      Column("company_name", String(5)),
                      Column("product", Integer),
                      Column("quantity", Integer),
                      Column("store", String(5)),
                      Column("review", String(10))
                      )
meta.create_all()

# create consumer and insert messages into the table
c = Consumer({"bootstrap.servers": "localhost:9092", "group.id": "example-consumer"})
c.subscribe(['SALES_REVIEWS_STREAM'])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        continue
    print(msg.value())

    val = json.loads(msg.value())
    insert = sales_reviews.insert().values(
        company_name=val['S_COMPANY_NAME'],
        product=val['S_PRODUCT'],
        quantity=val['QUANTITY'],
        store=val["S_STORE"],
        review=val["REVIEW"]
    )
    conn = engine.connect()
    conn.execute(insert)
    conn.close()
