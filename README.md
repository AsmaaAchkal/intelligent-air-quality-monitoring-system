# Intelligent Air Quality Monitoring System

Air quality is a major public health concern, particularly in urban and industrial environments. Poor air quality can contribute to respiratory and cardiovascular diseases and negatively impact quality of life.

This project combines **Internet of Things (IoT)** and **Artificial Intelligence (AI)** technologies to monitor air quality in real time, analyze environmental data automatically, and generate intelligent alerts when dangerous conditions are detected.

---

## Problem Statement

Traditional air quality monitoring solutions often face several limitations:

- Lack of continuous environmental monitoring
- Expensive and inaccessible measurement systems
- Difficulty interpreting raw sensor data
- Absence of automatic alerts in critical situations

**How can IoT and Artificial Intelligence be combined to monitor air quality in real time and generate reliable automatic alerts?**

---

## Proposed Solution

The proposed solution is an intelligent IoT-based air quality monitoring system built around an **ESP32 microcontroller**.

The system:

- Collects environmental data in real time
- Measures temperature, humidity, and gas concentration
- Transmits sensor data to a backend server
- Uses a Machine Learning model to classify air quality levels
- Displays information through an interactive dashboard
- Generates alerts when air quality becomes hazardous

---

## System Architecture

The solution is composed of three main layers:

### IoT Layer

- ESP32 Microcontroller
- Temperature Sensor
- Humidity Sensor
- Gas Sensor
- Alert LED

### Backend & AI Layer

- Flask API
- Data Processing
- Air Quality Prediction Model
- JSON Communication

### Visualization Layer

- Streamlit Dashboard
- Real-Time Monitoring
- Historical Analysis
- Statistical Visualization
- Alert System

---

## Features

### Real-Time Monitoring

- Live display of sensor measurements
- Temperature monitoring
- Humidity monitoring
- Gas concentration monitoring
- Instant air quality prediction

### Historical Analysis

- Storage of collected measurements
- Historical tracking of environmental conditions
- Data review and monitoring over time

### Statistical Dashboard

- Interactive charts
- Air quality trends visualization
- Statistical summaries
- Environmental insights

### Intelligent Alerts

- Detection of abnormal conditions
- Air quality classification
- Automatic alert generation

---

## Machine Learning Model

The system uses a **Random Forest Classifier** trained on environmental data to predict air quality levels.

### Model Pipeline

1. Data Collection
2. Data Preprocessing
3. Feature Scaling
4. Model Training
5. Air Quality Prediction
6. Dashboard Visualization

---

## Technologies Used

- ESP32
- Python
- Flask
- Scikit-Learn
- Random Forest
- Streamlit
- Pandas
- NumPy
- Joblib

---

## Project Structure

```text
AIR_QUALITY_MONITORING/

├── air_quality_backend/
│   ├── app.py
│   ├── air_quality_history.csv
│   ├── random_forest_air_quality_model.joblib
│   ├── scaler.joblib
│   └── requirements.txt
│
├── air_quality_dashboard/
│   └── app_dashboard.py
│
├── Model/
│   ├── air_quality_model.ipynb
│   ├── final_air_quality_dataset_6000.csv
│   ├── random_forest_air_quality_model.joblib
│   └── scaler.joblib
│
├── screenshots/
│   ├── real-time-monitoring.png
│   ├── historical-analysis.png
│   └── statistics-dashboard.png
│
└── README.md
```

---

## Screenshots

### Real-Time Monitoring

![Real-Time Monitoring](screenshots/real-time-monitoring.png)

### Historical Analysis

![Historical Analysis](screenshots/historical-analysis.png)

### Statistics Dashboard

![Statistics Dashboard](screenshots/statistics-dashboard.png)

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/intelligent-air-quality-monitoring.git
cd intelligent-air-quality-monitoring
```

Install dependencies:

```bash
pip install -r air_quality_backend/requirements.txt
```

---

## Run the Backend API

```bash
cd air_quality_backend
python app.py
```

---

## Run the Dashboard

```bash
cd air_quality_dashboard
streamlit run app_dashboard.py
```

---

## Dataset

The machine learning model was trained using environmental data including:

- Temperature
- Humidity
- Gas concentration
- Air Quality Labels
