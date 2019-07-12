import requests
import json


class KafkaRest:

    def __init__(self, dns="localhost:8082", brokers="localhost:9092"):
        self.base = dns
        self.brokers = brokers
        self.headers = {"Accept": "application/vnd.kafka.v2+json",
                        "Content-Type": "application/vnd.kafka.v2+json"}
        self.ref = "https://docs.confluent.io/current/kafka-rest/api.html#topics"

    def get_topic(self, topic=None):
        """
        if no topic, returns a list of all topics; else returns metadata for given topic
        :param topic: existing topic
        :return:
        """
        if topic:
            url = self.base + "/topic/%s" % topic
        else:
            url = self.base + "/topic"

        r = requests.get(url, headers=self.headers)
        resp = json.loads(r.content)
        return resp
