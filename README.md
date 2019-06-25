# pyconfluent
pyconfluent brings most Confluent Kafka functionality to Python by providing wrappers for the KSQL and Schema Registry REST APIs, and an in-depth Pythonic interpretation of the Kafka Streams Java package inspired by Robinhood's `faust` and Winton's `winton-kafka-streams`.

### Installation
This package was written for Python 3.6 and was not tested on other versions.

`pip3 install pyconfluent`

### Usage

pyconfluent requires the Confluent Platform and all its underlying services to be running. When creating class instances, make sure to pass in the list of brokers running or leave it empty to connect to `localhost`. 

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
