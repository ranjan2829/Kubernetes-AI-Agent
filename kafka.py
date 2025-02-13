from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers="localhost:9092",
                         value_serializer=lambda v: json.dumps(v).encode("utf-8"))

logs = {"app_logs": "Error found!", "system_logs": "All good!"}
producer.send("logs_topic", logs)
