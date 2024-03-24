import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
from pandasgui import show
from get_latest_price_data import get_latest_price_data

def get_tickers(dataframe : pd.DataFrame) -> list:
    """Get the company tickers from a dataframe."""

    # Get the tickers from the 'ticker' column
    tickers = dataframe['ticker'].tolist()

    return tickers

def fetch_data():
    """Fetch the company data and present it in a GUI."""
    
    csv_file = 'MoS-Calculator/companies.csv'
    df = pd.read_csv(csv_file)
    
    # Get tickers for the companies
    tickers = get_tickers(df)

    # Fetch the latest price data for the companies
    price_data = get_latest_price_data(tickers)

    df['currentPrice'] = df['ticker'].map(price_data)

    # Calculate motivated price for 2024 and 2025
    df['motivatedPrice2024'] = df.apply(lambda row: row.eps2024e * row.motivatedPE, axis=1)
    df['motivatedPrice2025'] = df.apply(lambda row: row.eps2025e * row.motivatedPE, axis=1)

    # Calculate margin of safety for 2024 and 2025
    df['MoS2024'] = round(1 - df['currentPrice'] / df['motivatedPrice2024'], 2) 
    df['MoS2025'] = round(1 - df['currentPrice'] / df['motivatedPrice2025'], 2) 

    return df

def present_data(dataframe : pd.DataFrame) -> None:
    show(dataframe)

def main():
    # Call the fetch_data function to fetch the data and present it in a GUI
    data = fetch_data()
    present_data(data)

if __name__ == "__main__":
    main()