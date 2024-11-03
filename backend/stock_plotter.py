import matplotlib.pyplot as plt
import plotly.graph_objects as go

class StockPlotter:
    def __init__(self, ticker, start_date, end_date, data):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = data

    def plot_rsi(self):
        """Plot the RSI along with overbought and oversold lines and stock price overlay."""
        if 'RSI' not in self.data.columns:
            raise ValueError("RSI not calculated. Please calculate RSI before plotting.")

        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Plotting RSI
        ax1.plot(self.data.index, self.data['RSI'], label='RSI', color='blue')
        ax1.axhline(30, color='red', linestyle='dotted', linewidth=1, label='Oversold (30)')
        ax1.axhline(70, color='green', linestyle='dotted', linewidth=1, label='Overbought (70)')
        ax1.set_ylim(0, 100)
        ax1.set_ylabel("RSI")
        ax1.set_title(f"RSI and Stock Price for {self.ticker} from {self.start_date} to {self.end_date}")
        ax1.legend(loc="upper left")
        ax1.grid()

        # Overlaying stock price
        ax2 = ax1.twinx()  # Secondary y-axis for stock price
        ax2.plot(self.data.index, self.data['Close'], label='Stock Price', color='black', alpha=0.5)
        ax2.set_ylabel("Stock Price")
        ax2.legend(loc="upper right")

        plt.show()

    def plot_macd(self):
        """Plot the MACD and signal line with stock price overlay using a secondary y-axis."""
        if 'MACD' not in self.data.columns or 'Signal_Line' not in self.data.columns:
            raise ValueError("MACD not calculated. Please calculate MACD before plotting.")

        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Add MACD line (on primary y-axis)
        ax1.plot(self.data.index, self.data['MACD'], label='MACD', color='blue')
        
        # Add Signal Line (on primary y-axis)
        ax1.plot(self.data.index, self.data['Signal_Line'], label='Signal Line', color='orange')

        # Add horizontal line at zero (on primary y-axis)
        ax1.axhline(0, color='black', linestyle='dashed', linewidth=1)  # Zero line

        # Configure primary y-axis
        ax1.set_title(f"MACD and Stock Price for {self.ticker} from {self.start_date} to {self.end_date}")
        ax1.set_ylabel("MACD")
        ax1.legend(loc="upper left")
        ax1.grid()

        # Overlaying stock price on secondary y-axis
        ax2 = ax1.twinx()  # Secondary y-axis for stock price
        ax2.plot(self.data.index, self.data['Close'], label='Stock Price', color='black', alpha=0.5)
        ax2.set_ylabel("Stock Price")
        ax2.legend(loc="upper right")

        plt.show()
