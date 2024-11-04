# StockGPT

StockGPT is an AI-powered tool designed to summarize financial statements, making financial analysis faster and more accessible. Created for analysts and investors, it aims to save time and reduce redundancy in analyzing stocks by generating fundamental and technical analyses, along with investment recommendations.
## Project Overview

StockGPT assists financial analysts by automating parts of the stock analysis process. With just a stock ticker, StockGPT provides:

* A fundamental analysis of the stock
* A technical analysis of recent performance
* An overview of the company’s profile
* Investment suggestions based on AI-driven insights

## Built With

* **Frontend**: Svelte, TailwindCSS
* **Backend**: Python (Flask)
* **AI Integration**: AWS Bedrock
* **Data Source**: Yahoo Finance API (`yfinance`)

## Getting Started
### Prerequisites

* AWS credentials are required for accessing Bedrock for AI functionalities.

### Installation

1. Clone the repository:
    ```
    git clone https://github.com/LoicDG/Datathon_2024.git
    cd Datathon_2024
    ```

2. Install dependencies:
    ```
    pip install -r backend/requirements.txt
    cd frontend
    npm install
    ```

3. Set up AWS credentials:
    * Configure AWS credentials locally to enable interaction with AWS Bedrock.

## Running the Project

Start the backend server (from the `backend` folder):

* open the file named llm.ipynb
* run the entire jupyter notebook, wait a couple minutes for it to start

Run the Svelte frontend (from the `frontend` folder):

```
npm run dev
```

The website should now be accessible at `http://localhost:5173`.
## Usage

1. Enter the ticker symbol of a stock (e.g., AAPL for Apple).
2. StockGPT will generate:
    * A fundamental analysis (financial ratios, performance metrics)
    * A technical analysis (trends, price movements)
    * An overview of the company
    * A suggested action (e.g., buy, hold, sell)

## Challenges & Lessons Learned

As a team new to AWS, navigating the environment and connecting to AWS Bedrock was a significant learning experience. We encountered challenges in integrating the AI models and fine-tuning data retrieval to meet our analysis criteria.

## Hackathon

StockGPT was developed during the **2024 Datathon** by Polyfinances.
## Contributors

* **Loic Desrochers-Girard**
* **Clara Dakessian**
* **Jason Xa**
* **Maya Hammamouche**