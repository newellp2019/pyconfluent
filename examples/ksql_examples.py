from pyconfluent.ksql import KSQL

k = KSQL()

sales_q = "CREATE STREAM sales_stream (company VARCHAR, product INT, quantity INT) " \
          "WITH (KAFKA_TOPIC='sales', VALUE_FORMAT='DELIMITED')"
sales_stream = k.ksql(sales_q)
print(sales_stream)
