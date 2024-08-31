import pandas as pd
import numpy as np
from pmdarima import auto_arima
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("Stock_prediction\Stock_Price_data_set.csv")

# Convert 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Set 'Date' column as index
df.set_index('Date', inplace=True)

# Split data into training and testing sets
train_size = int(len(df) * 0.8)
train_data, test_data = df[:train_size], df[train_size:]

# Fit SARIMA model
model = auto_arima(train_data['Close'], seasonal=True, m=12, trace=True)

# Make predictions
forecast, conf_int = model.predict(n_periods=len(test_data), return_conf_int=True)
forecast_index = pd.date_range(start=test_data.index[0], periods=len(test_data))
print("Prediction values:", forecast)


# Plot actual vs predicted
plt.figure(figsize=(10, 5))
plt.plot(train_data.index, train_data['Close'], label='Training')
plt.plot(test_data.index, test_data['Close'], label='Actual')
plt.plot(forecast_index, forecast, label='Predicted')
plt.fill_between(forecast_index, conf_int[:, 0], conf_int[:, 1], color='k', alpha=0.1)
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.title('Actual vs Predicted Stock Prices (SARIMA)')
plt.legend()
plt.show()
