import os
import boto3
import json
import time
from botocore.exceptions import BotoCoreError, ClientError
from stock_analysis import StockAnalysis  # Ensure this class is correctly defined

# AWS configuration (credentials should be stored in environment variables)
DEFAULT_REGION = "us-west-2"
ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
SECRET_KEY = os.getenv("AWS_SECRET_KEY")
SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")

# Check for credentials in environment variables
if not ACCESS_KEY or not SECRET_KEY or not SESSION_TOKEN:
    print("AWS credentials not found in environment variables. Exiting.")
    exit(1)

# Initialize the Bedrock client with secure credentials
try:
    client = boto3.client(
        'bedrock-runtime',
        region_name=DEFAULT_REGION,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN
    )
except (BotoCoreError, ClientError) as e:
    print(f"Error initializing AWS client: {e}")
    exit(1)  # Exit if the client cannot be initialized

# Specify stock ticker and date range with input validation
ticker = "AAPL"
start_date = "2023-02-13"
end_date = "2024-11-02"

# Validate date format (basic validation)
try:
    from datetime import datetime
    datetime.strptime(start_date, "%Y-%m-%d")
    datetime.strptime(end_date, "%Y-%m-%d")
except ValueError:
    print("Invalid date format. Please use YYYY-MM-DD.")
    exit(1)

# Create an instance of StockAnalysis
stock_analysis = StockAnalysis(ticker=ticker, start_date=start_date, end_date=end_date)

# Download data and calculate indicators
stock_analysis.download_data()
stock_analysis.calculate_rsi(period=14)
stock_analysis.calculate_macd()

# Get RSI and MACD data for further analysis
rsi_data = stock_analysis.get_rsi_data()
macd_data = stock_analysis.get_macd_data()

# Prepare MACD and RSI data for prompt inclusion using list comprehensions
macd_analysis = [
    f"Date: {entry['Date'].strftime('%Y-%m-%d')}, MACD: {entry['MACD']:.2f}, Signal Line: {entry['Signal Line']:.2f}"
    for entry in macd_data.to_dict(orient='records')
]

rsi_analysis = [
    f"Date: {entry['Date'].strftime('%Y-%m-%d')}, RSI: {entry['RSI']:.2f}"
    for entry in rsi_data.to_dict(orient='records')
]

# Formulate the AI prompt with additional data
body = json.dumps({
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 1000,
    "messages": [
        {
            "role": "user",
            "content": (
                f"Create a technical analysis report for {ticker} from {start_date} to {end_date}. Include: "
                "1. Indicators: Moving Averages, "
                f"Recent RSI indicator analysis: {', '.join(rsi_analysis)}, "
                f"Recent MACD values indicator analysis: {', '.join(macd_analysis)}. "
                "2. Analysis of trends and events affecting the stock. "
                "3. Clear conclusion on whether to buy, hold, or sell. "
                "Use clear, technical market terminology."
            )
        }
    ]
})

# Retry configuration with exponential backoff
MAX_RETRIES = 5
INITIAL_BACKOFF = 1  # Start with a 1-second delay

# Attempt to invoke the model with retry logic
for attempt in range(MAX_RETRIES):
    try:
        response = client.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            contentType="application/json",
            accept="application/json",
            body=body
        )

        # Process response if successful
        resp_str = response.get('body').read().decode('utf-8')
        print(resp_str)
        break  # Exit loop if successful

    except client.exceptions.ThrottlingException as e:
        delay = INITIAL_BACKOFF * (2 ** attempt)
        print(f"Throttling error: {e}. Retrying in {delay} seconds...")
        time.sleep(delay)  # Exponential backoff

    except (BotoCoreError, ClientError) as e:
        print(f"Error invoking AI model: {e}")
        break  # Exit loop if it's a non-throttling exception

    except Exception as e:
        print(f"Unexpected error: {e}")
        break  # Exit loop on any other unexpected errors
