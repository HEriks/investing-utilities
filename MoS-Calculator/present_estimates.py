import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
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
    df['MoS2024'] = 1 - df['motivatedPrice2024'] / df['currentPrice']
    df['MoS2025'] = 1 - df['motivatedPrice2025'] / df['currentPrice']

    return df

def present_data(dataframe : pd.DataFrame) -> None:
    # Create a GUI window
    window = tk.Tk()
    window.title("Margin of Safety")

    # Create a DataFrame to store the margin of safety data
    mos_data = df[['ticker', 'MoS2024', 'MoS2025']]

    # Create a Treeview widget to display the data
    tree = ttk.Treeview(window)
    tree["columns"] = ("MoS2024", "MoS2025")
    tree.heading("#0", text="Ticker")
    tree.heading("MoS2024", text="MoS 2024")
    tree.heading("MoS2025", text="MoS 2025")

    # Insert the data into the Treeview widget
    for index, row in mos_data.iterrows():
        ticker = row['ticker']
        mos_2024 = row['MoS2024']
        mos_2025 = row['MoS2025']
        tree.insert("", "end", text=ticker, values=(mos_2024, mos_2025))

    # Add the Treeview widget to the window
    tree.pack()

    # Start the GUI event loop
    window.mainloop()

def main():
    # Call the fetch_data function to fetch the data and present it in a GUI
    data = fetch_data()
    present_data(data)

if __name__ == "__main__":
    main()