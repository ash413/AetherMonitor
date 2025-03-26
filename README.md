# AetherMonitor

## Overview

AetherMonitor is a cloud-based IoT system for real-time environmental monitoring using AWS IoT Core, DynamoDB, and Streamlit. This project simulates an environmental station that publishes sensor data via MQTT, stores it in AWS DynamoDB, and visualizes it using Streamlit.

## Features

- Simulated virtual environmental station publishing data via MQTT
- AWS IoT Core as the message broker
- AWS DynamoDB for cloud storage
- Real-time data visualization using Streamlit
- Displays latest sensor data and historical data for the last 5 hours

## Tech Stack

- AWS IoT Core (MQTT message broker)
- AWS DynamoDB (NoSQL database for sensor data storage)
- Python (Data processing and visualization)
- Paho-MQTT (For MQTT client communication)
- Boto3 (AWS SDK for Python)
- Streamlit (For real-time data visualization)

## Installation and Setup

### Prerequisites

- Python 3.8+
- AWS IoT Core setup with MQTT topics
- AWS DynamoDB table (SensorData) created
- AWS credentials configured via AWS CLI (aws configure)

### Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/AetherMonitor.git
cd AetherMonitor
```

2. Install dependencies:
```
pip3 install paho-mqtt boto3 plotly streamlit
```

3. Set up AWS credentials and configure IoT Core certificates.

4. Run the MQTT client to publish data:
```
python mqttclient.py
```

5. Run the Streamlit dashboard:
```
streamlit run dashboard.py
```

## Usage

- The MQTT client simulates a virtual environmental station and publishes temperature, humidity, and CO2 data.

- The Streamlit dashboard fetches data from DynamoDB and visualizes it in real-time.

## Future Enhancements

- Implement real IoT sensors for live data collection

- Use AWS Lambda for automated data processing

- Deploy Streamlit app on AWS EC2 or AWS App Runner