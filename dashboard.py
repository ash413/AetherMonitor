import streamlit as st
import boto3
from boto3.dynamodb.conditions import Key
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# AWS DynamoDB Configuration
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('SensorData')

def fetch_sensor_data(hours=5):
    """
    Fetch sensor data from the last specified number of hours
    """
    # Calculate timestamp for 5 hours ago
    five_hours_ago = int(datetime.now().timestamp()) - (hours * 3600)
    
    # Query DynamoDB for data in the last 5 hours
    response = table.scan(
        FilterExpression=Key('timestamp').gte(str(five_hours_ago))
    )
    
    # Convert response to DataFrame
    df = pd.DataFrame(response['Items'])
    
    # Convert timestamp and numeric columns
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'].astype(int), unit='s')
        df['temperature'] = df['temperature'].astype(float)
        df['humidity'] = df['humidity'].astype(float)
        df['co2'] = df['co2'].astype(int)
    
    return df

def create_dashboard():
    """
    Streamlit dashboard for IoT sensor data visualization
    """
    st.title('IoT Environmental Monitoring Dashboard')
    
    # Fetch sensor data
    df = fetch_sensor_data()
    
    if df.empty:
        st.warning('No sensor data available')
        return
    
    # Latest Sensor Readings Section
    st.header('Latest Sensor Readings')
    latest_reading = df.iloc[-1]
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric('Temperature', f"{latest_reading['temperature']}°C")
    with col2:
        st.metric('Humidity', f"{latest_reading['humidity']}%")
    with col3:
        st.metric('CO2', f"{latest_reading['co2']} ppm")
    
    # Time Series Plots
    st.header('Sensor Data Trends (Last 5 Hours)')
    
    # Temperature Plot
    fig_temp = px.line(df, x='timestamp', y='temperature', 
                       title='Temperature Over Time',
                       labels={'temperature': 'Temperature (°C)', 'timestamp': 'Time'})
    st.plotly_chart(fig_temp)
    
    # Humidity Plot
    fig_humid = px.line(df, x='timestamp', y='humidity', 
                        title='Humidity Over Time',
                        labels={'humidity': 'Humidity (%)', 'timestamp': 'Time'})
    st.plotly_chart(fig_humid)
    
    # CO2 Plot
    fig_co2 = px.line(df, x='timestamp', y='co2', 
                      title='CO2 Levels Over Time',
                      labels={'co2': 'CO2 (ppm)', 'timestamp': 'Time'})
    st.plotly_chart(fig_co2)
    
    # Raw Data Table
    st.header('Raw Sensor Data')
    st.dataframe(df)

if __name__ == '__main__':
    create_dashboard()