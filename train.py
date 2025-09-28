import pandas as pd
import os
import joblib
from statsmodels.tsa.arima.model import ARIMA


# Load dataset
df = pd.read_excel("commodity_price.xlsx")
df.columns = df.columns.str.strip()
df.rename(columns={'Arrival_Date': 'Date'}, inplace=True)
# Rename commodity column
if 'Commodi' in df.columns:
    df.rename(columns={'Commodi': 'Commodity'}, inplace=True)

# Rename Modal Price column
if 'Modal_x0020_Price' in df.columns:
    df.rename(columns={'Modal_x0020_Price': 'ModalPrice'}, inplace=True)

# Rename your actual date column to 'Date'
if 'Arrival_Date' in df.columns:
    df.rename(columns={'Arrival_Date': 'Date'}, inplace=True)
elif 'al_Date' in df.columns:
    df.rename(columns={'al_Date': 'Date'}, inplace=True)
elif 'Date_x0020' in df.columns:
    df.rename(columns={'Date_x0020': 'Date'}, inplace=True)

# Now convert to datetime
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
