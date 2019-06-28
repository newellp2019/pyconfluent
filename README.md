# pyconfluent
pyconfluent brings most Confluent Kafka functionality to Python by providing wrappers for the KSQL and Schema Registry REST APIs.

### Installation
This package was written for Python 3.6 and was not tested on other versions.

`pip3 install pyconfluent`

### Usage

pyconfluent requires the Confluent Platform and all its underlying services to be running. When creating class instances, make sure to pass in the list of brokers running or leave it empty to connect to `localhost`. 

### KSQL

```
from pyconfluent.ksql import KSQL

k = KSQL()

# create the 2 streams from existing topics
sales_stream = k.ksql("CREATE STREAM sales_stream (company_name VARCHAR, product BIGINT, quantity BIGINT, "
                      "store VARCHAR) WITH (KAFKA_TOPIC='sales', VALUE_FORMAT='JSON');")
reviews_stream = k.ksql("CREATE STREAM reviews_stream (company_name VARCHAR, product BIGINT, review VARCHAR, "
                        "store VARCHAR) WITH (KAFKA_TOPIC='reviews', VALUE_FORMAT='JSON');")

# JOIN the two to create a persistent, enriched stream
sales_reviews_stream = k.ksql("CREATE STREAM sales_reviews_stream AS SELECT "
                              "s.company_name, s.product, s.quantity, s.store, "
                              "review FROM sales_stream s "
                              "INNER JOIN reviews_stream r WITHIN 1 SECONDS "
                              "ON s.product = r.product; ")

```
