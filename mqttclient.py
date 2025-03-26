from decimal import Decimal
import boto3
import time
import json
import random
import paho.mqtt.client as mqtt
import ssl
from datetime import datetime

# AWS IoT Core Endpoint (found under "Settings" in AWS IoT Console)
AWS_ENDPOINT = "afrtojad58wck-ats.iot.us-east-1.amazonaws.com"
THING_NAME = "VirtualEnvStation1"
TOPIC = "env/station1/data"

# Paths to certificates downloaded from AWS IoT
CERT_PATH = "certificate.pem.crt"
KEY_PATH = "private.pem.key"
ROOT_CA_PATH = "AmazonRootCA1.pem"

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('SensorData')

# Function to generate random sensor values (Convert to Decimal for DynamoDB)
def generate_sensor_data():
    return {
        "station_id": THING_NAME,
        "timestamp": str(int(time.time())),  # Convert timestamp to string
        "temperature": Decimal(str(round(random.uniform(-50, 50), 2))),  # Convert to Decimal
        "humidity": Decimal(str(round(random.uniform(0, 100), 2))),  # Convert to Decimal
        "co2": Decimal(str(random.randint(300, 2000)))  # Convert to Decimal
    }

# Function to publish sensor data
def publish_data():
    sensor_data = generate_sensor_data()

    # Convert Decimal to float for MQTT publishing
    sensor_data_mqtt = {
        "station_id": sensor_data["station_id"],
        "timestamp": sensor_data["timestamp"],
        "temperature": float(sensor_data["temperature"]),  # Convert back to float
        "humidity": float(sensor_data["humidity"]),
        "co2": int(sensor_data["co2"])  # Convert to int
    }

    # Publish to MQTT
    client.publish(TOPIC, json.dumps(sensor_data_mqtt))
    print(f"Published: {sensor_data_mqtt}")

    # Store data in DynamoDB
    table.put_item(Item=sensor_data)

# MQTT Setup
client = mqtt.Client(client_id=THING_NAME)
client.tls_set(ROOT_CA_PATH, certfile=CERT_PATH, keyfile=KEY_PATH, tls_version=ssl.PROTOCOL_TLSv1_2)
client.connect(AWS_ENDPOINT, 8883, 60)

# Publish sensor data every 10 seconds
while True:
    publish_data()
    time.sleep(10)