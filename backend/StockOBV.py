import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

class StockOBV:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = None

    def download_data(self):
        """Download historical stock data."""
        self.data = yf.download(self.ticker, start=self.start_date, end=self.end_date)

    def calculate_obv(self):
        """Calculate On-Balance Volume (OBV)."""
        if self.data is not None:
            # Calculate daily price change
            price_change = self.data['Close'].diff()

            # Calculate OBV
            self.data['OBV'] = (price_change > 0).astype(int) * self.data['Volume'] - (price_change < 0).astype(int) * self.data['Volume']
            self.data['OBV'] = self.data['OBV'].cumsum()  # Cumulative sum to get OBV
        else:
            raise ValueError("Data not downloaded. Please call download_data() first.")

    def get_obv_data(self):
        """Return a DataFrame of dates and their corresponding OBV values."""
        if 'OBV' not in self.data.columns:
            raise ValueError("OBV not calculated. Please call calculate_obv() first.")
        
        # Create a DataFrame with the date and OBV values
        obv_data = self.data[['OBV']].dropna().reset_index()
        obv_data.columns = ['Date', 'OBV']  # Rename columns for clarity
        
        return obv_data

    def plot_obv(self):
        """Plot the OBV along with the closing price."""
        if 'OBV' not in self.data.columns:
            raise ValueError("OBV not calculated. Please call calculate_obv() first.")

        plt.figure(figsize=(12, 6))
        plt.plot(self.data.index, self.data['OBV'], label='OBV', color='blue')
        plt.title(f"On-Balance Volume (OBV) for {self.ticker} Stock from {self.start_date} to {self.end_date}")
        plt.xlabel("Date")
        plt.ylabel("OBV")
        plt.legend()
        plt.grid()

        # Show the plot
        plt.show()

# Example usage
if __name__ == "__main__":
    # Initialize the StockOBV class
    stock_obv = StockOBV(ticker="AAPL", start_date="2020-02-13", end_date="2024-03-13")

    # Download data, calculate OBV, and plot
    stock_obv.download_data()
    stock_obv.calculate_obv()
    stock_obv.plot_obv()

    # Get OBV data for further analysis
    obv_data = stock_obv.get_obv_data()
    print(obv_data)  # Print or save the OBV data as needed
