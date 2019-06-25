# py-confluent
Bringing KSQL, Kafka Streams, Schema Registry APIs to Python 3,
all in one clean package.

### Install

`pip install pyconfluent`

### Usage

pyconfluent requires the underlying Kafka services to be running. The 
easiest way is to start Confluent Platform, see: ``.

### KSQL

```
import KSQL

k = KSQL()  # enter your boostrap_server here if not 'localhost', no port

# create streams from existing topics
sales_stream = k.ksql("CREATE STREAM sales (company VARCHAR, product BIGINT, quantity BIGINT)"
                      "WITH (KAFKA_TOPIC='sales', VALUE_FORMAT='JSON';")

reviews_stream = k.ksql("CREATE STREAM reviews (company VARCHAR, product BIGINT, review VARCHAR)"
                        "WITH (KAFKA_TOPIC='sales', VALUE_FORMAT='JSON';")

# stream to stream join, WITHIN clause required
# creates and populates new kafka topic
enriched_stream = k.ksql("CREATE STREAM enriched AS SELECT"
                         "sales.company, sales.product, sales.quantity"
                         "FROM sales LEFT JOIN reviews WITH 1 HOURS"
                         "ON sales.company = reviews.company")

```
