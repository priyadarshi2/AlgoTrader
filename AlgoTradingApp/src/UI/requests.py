import streamlit as st
import requests
import pandas as pd

def common_backtest_ui():
    # Streamlit app title
    st.title("Common Strategies Backtest")

    # Input fields for parameters
    symbol = st.text_input("Ticker Symbol", placeholder="e.g., AAPL")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    amount = st.number_input("Investment Amount", min_value=0.0, format="%f", value=1000.0)

    # Fetch available strategies from backend
    st.sidebar.title("Available Strategies")
    strategies_url = "http://127.0.0.1:8000/common-strategies"
    strategies_response = requests.get(strategies_url)

    if strategies_response.status_code == 200:
        strategies = strategies_response.json()
        strategies = strategies["data"]
        strategy_keys = list(strategies.keys())
        strategy_values = list(strategies.values())
        selected_strategy = st.sidebar.selectbox(
            "Select Strategy",
            strategy_values
        )
        pos = strategy_values.index(selected_strategy)  # Extract the key
        backtest_key = strategy_keys[pos]
    else:
        st.sidebar.error("Failed to fetch strategies.")
        return

    # Button to run the backtest
    if st.button("Run Backtest"):
        if not symbol or not start_date or not end_date:
            st.error("Please enter all required fields.")
        elif start_date > end_date:
            st.error("Start date cannot be after the end date.")
        else:
            # Convert dates to ISO format strings
            start_date_str = start_date.isoformat()
            end_date_str = end_date.isoformat()

            # Define the URL of your FastAPI endpoint
            url = "http://127.0.0.1:8000/common-backtest"

            # Define the query parameters
            params = {
                "ticker_symbol": symbol,
                "start_date": start_date_str,
                "end_date": end_date_str,
                "amount": amount,
                "key": backtest_key
            }

            # Send a GET request to the FastAPI endpoint
            with st.spinner("Running backtest..."):
                response = requests.get(url, params=params)

            if response.status_code == 200:
                # Display the backtest results
                result = response.json()
                st.success("Backtest completed successfully!")

                # Display the summary
                st.write("### Summary")
                summary = result['summary']
                for key, value in summary.items():
                    st.markdown(f"**{key.capitalize()}:** {value}")

                # Convert trade history to DataFrame
                st.write("### Trade History")
                trades_df = pd.DataFrame(result['hist'])
                st.dataframe(trades_df)

            elif response.status_code == 400:
                st.error(f"Bad Request: {response.json().get('detail', 'Unknown error')}")
            elif response.status_code == 406:
                st.error(f"Validation Error: {response.json().get('detail', 'Unknown error')}")
            else:
                st.error(f"Error {response.status_code}: {response.text}")
