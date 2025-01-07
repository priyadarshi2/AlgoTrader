import streamlit as st
import requests
import pandas as pd

# Define the backend endpoints
STRATEGIES_URL = "http://127.0.0.1:8000/common-strategies"
PARAMETERS_URL = "http://127.0.0.1:8000/get-parameter?key="
BACKTEST_URL = "http://127.0.0.1:8000/common-backtest"

def fetch_strategies():
    """Fetch available strategies from the backend."""
    try:
        response = requests.get(STRATEGIES_URL)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            st.sidebar.error("Failed to fetch strategies.")
            return {}
    except Exception as e:
        st.sidebar.error(f"Error fetching strategies: {e}")
        return {}

def fetch_parameters(key):
    """Fetch strategy parameters based on the selected key."""
    try:
        response = requests.get(PARAMETERS_URL + str(key))
        if response.status_code == 200:
            return response.json()["data"]
        else:
            st.error("Failed to fetch parameters. Please check the key and try again.")
            return {}
    except Exception as e:
        st.error(f"Error fetching parameters: {e}")
        return {}

def run_backtest(params_dict):
    """Send a GET request to the backend to execute the backtest."""
    try:
        response = requests.get(BACKTEST_URL, params=params_dict)
        return response
    except Exception as e:
        st.error(f"Error running backtest: {e}")
        return None

def common_backtest_ui():
    # Streamlit app title
    st.title("Common Strategies Backtest")

    # Input fields for backtest parameters
    symbol = st.text_input("Ticker Symbol", placeholder="e.g., AAPL")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    amount = st.number_input("Investment Amount", min_value=0.0, value=1000.0)

    # Fetch available strategies
    st.sidebar.title("Available Strategies")
    strategies = fetch_strategies()

    if strategies:
        # Strategy selection
        strategy_keys = list(strategies.keys())
        strategy_values = list(strategies.values())
        selected_strategy = st.sidebar.selectbox("Select Strategy", strategy_values)
        backtest_key = strategy_keys[strategy_values.index(selected_strategy)]

        # Fetch and display strategy parameters
        st.sidebar.header("Parameter Settings")
        params = fetch_parameters(backtest_key)
        param_values = {}

        if params:
            # Assuming params is a list, and we need to display sliders or inputs for each
            for param in params:  # `params` is a list now
                param_name = param  # Adjust based on the response structure

                #####CORRECT IT PARAM NAME shouldn't be INTEGER
                on = st.sidebar.checkbox(f"Adjust : {param_name}", value=False)
                if on:
                    param_values[param_name] = st.sidebar.slider(param_name, min_value=1, max_value=100, value=10)
                print(param_values)

        else:
            st.sidebar.warning("No parameters available for this strategy.")

        # Run backtest button
        if st.button("Run Backtest"):
            # Validate inputs
            if not symbol or not start_date or not end_date:
                st.error("Please enter all required fields.")
            elif start_date > end_date:
                st.error("Start date cannot be after the end date.")
            else:
                # Convert dates to ISO format strings
                start_date_str = start_date.isoformat()
                end_date_str = end_date.isoformat()

                # Build query parameters for the request
                params_dict = {
                    "ticker_symbol": symbol,
                    "start_date": start_date_str,
                    "end_date": end_date_str,
                    "amount": amount,
                    "key": backtest_key
                }

                # Add strategy parameters to the request
                params_dict.update(param_values)

                # Debugging: Display the parameters being sent
                #st.write("Request Parameters:", params_dict)

                # Send request to the backend
                with st.spinner("Running backtest..."):
                    response = run_backtest(params_dict)

                # Handle response
                if response:
                    if response.status_code == 200:
                        result = response.json()
                        st.success("Backtest completed successfully!")

                        # Display summary
                        st.write("### Summary")
                        for key, value in result['summary'].items():
                            st.markdown(f"**{key.capitalize()}:** {value}")

                        # Display trade history
                        st.write("### Trade History")
                        trades_df = pd.DataFrame(result['hist'])
                        st.dataframe(trades_df)

                    elif response.status_code == 400:
                        st.error(f"Bad Request: {response.json().get('detail', 'Unknown error')}")
                    elif response.status_code == 406:
                        st.error(f"Validation Error: {response.json().get('detail', 'Unknown error')}")
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
                else:
                    st.error("Failed to connect to the backend.")
