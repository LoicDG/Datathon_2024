import yfinance as yf
import pandas as pd
from stock_plotter import StockPlotter  # Import the StockPlotter class

class StockAnalysis:
    def __init__(self, ticker: str, start_date: str, end_date: str):
        """
        Initialize StockAnalysis with a ticker symbol, start date, and end date.
        """
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = None
        self.plotter = StockPlotter(ticker, start_date, end_date, self.data)  # Initialize the plotter

    def download_data(self) -> None:
        """
        Download historical stock data with a buffer for indicators.
        """
        # 26 days buffer to ensure initial values stabilize, especially for MACD
        buffer_days = 26
        start_with_buffer = pd.to_datetime(self.start_date) - pd.Timedelta(days=buffer_days)
        self.data = yf.download(self.ticker, start=start_with_buffer.strftime('%Y-%m-%d'), end=self.end_date)
        
        # Update plotter data
        self.plotter.data = self.data  

    def calculate_rsi(self, period: int = 14) -> None:
        """
        Calculate the Relative Strength Index (RSI) for the stock data.
        """
        if self.data is None:
            raise ValueError("Data not downloaded. Please call download_data() first.")
        
        delta = self.data['Close'].diff()
        gains = delta.where(delta > 0, 0)
        losses = -delta.where(delta < 0, 0)
        
        avg_gain = gains.ewm(span=period, min_periods=period).mean()
        avg_loss = losses.ewm(span=period, min_periods=period).mean()
        
        rs = avg_gain / avg_loss
        self.data['RSI'] = 100 - (100 / (1 + rs))

    def calculate_macd(self, short_window: int = 12, long_window: int = 26, signal_window: int = 9) -> None:
        """
        Calculate the Moving Average Convergence Divergence (MACD) and the Signal Line.
        """
        if self.data is None:
            raise ValueError("Data not downloaded. Please call download_data() first.")
        
        # Calculating the short and long Exponential Moving Averages (EMAs)
        self.data['Short_EMA'] = self.data['Close'].ewm(span=short_window, adjust=False).mean()
        self.data['Long_EMA'] = self.data['Close'].ewm(span=long_window, adjust=False).mean()
        
        # Calculate MACD and Signal Line
        self.data['MACD'] = self.data['Short_EMA'] - self.data['Long_EMA']
        self.data['Signal_Line'] = self.data['MACD'].ewm(span=signal_window, adjust=False).mean()

        # Remove the buffer rows to avoid misleading initial values
        self.data = self.data.loc[self.start_date:]

    def get_rsi_data(self) -> pd.DataFrame:
        """
        Return a DataFrame of dates and their corresponding RSI values.
        """
        if 'RSI' not in self.data.columns:
            raise ValueError("RSI not calculated. Please call calculate_rsi() first.")
        
        rsi_data = self.data[['RSI']].dropna().reset_index()
        rsi_data.columns = ['Date', 'RSI']
        return rsi_data

    def get_macd_data(self) -> pd.DataFrame:
        """
        Return a DataFrame of dates and their corresponding MACD and Signal Line values.
        """
        if 'MACD' not in self.data.columns or 'Signal_Line' not in self.data.columns:
            raise ValueError("MACD not calculated. Please call calculate_macd() first.")
        
        macd_data = self.data[['MACD', 'Signal_Line']].dropna().reset_index()
        macd_data.columns = ['Date', 'MACD', 'Signal Line']
        return macd_data

# Example usage
if __name__ == "__main__":
    stock_analysis = StockAnalysis(ticker="RBLX", start_date="2023-02-13", end_date="2025-11-02")
    stock_analysis.download_data()
    
    # Calculate indicators
    stock_analysis.calculate_rsi(period=14)
    stock_analysis.calculate_macd()
    
    # Plot RSI and MACD
    stock_analysis.plotter.plot_rsi()
    stock_analysis.plotter.plot_macd()
    
    # Get RSI and MACD data for further analysis
    rsi_data = stock_analysis.get_rsi_data()
    print("RSI Data:\n", rsi_data)
    
    macd_data = stock_analysis.get_macd_data()
    print("MACD Data:\n", macd_data)
