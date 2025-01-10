import streamlit as st
import requests
import pandas as pd

# Define the backend endpoints
STRATEGIES_URL = "http://127.0.0.1:8000/common-strategies"
PARAMETERS_URL = "http://127.0.0.1:8000/get-parameter?key="
BACKTEST_URL = "http://127.0.0.1:8000/common-backtest"
PARAM_VALIDATION_URL = "http://127.0.0.1:8000/param-validation"

def fetch_strategies():
    """Fetch available strategies from the backend."""
    try:
        response = requests.get(STRATEGIES_URL)
        print("response==>",response.json()["data"])
        if response.status_code == 200:
            return response.json()["data"]
        else:
            st.sidebar.error("Failed to fetch strategies.")
            return {}
    except Exception as e:
        st.sidebar.error(f"Error fetching strategies: {e}")
        return {}

def fetch_parameters(selected_strategy):
    """Fetch strategy parameters based on the selected key."""
    try:
        response = requests.get(PARAMETERS_URL + str(selected_strategy))
        if response.status_code == 200:
            return response.json()["data"]
        else:
            st.error("Failed to fetch parameters. Please check the key and try again.")
            return {}
    except Exception as e:
        st.error(f"Error fetching parameters: {e}")
        return {}

def run_backtest(paramets):
    """Send a GET request to the backend to execute the backtest."""
    try:
        response = requests.post(BACKTEST_URL, json=paramets)
        return response
    except Exception as e:
        st.error(f"Error running backtest: {e}")
        return None

def validate_params(paramets):
    """Send a GET request to the backend to validate the parameters."""

    try:
        response = requests.post(PARAM_VALIDATION_URL, json=paramets)
        if response.status_code == 200:
            return response
        else:
            st.error(f"Error validating parameters: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error validating parameters: {e}")
        return None



def common_backtest_ui():
    # Streamlit app title
    st.title("Common Strategies Backtest")

    intervals = {
        "1 Minute" : "1m",
        "2 Minutes" : "2m",
        "5 Minutes" : "5m",
        "15 Minutes" : "15m",
        "30 Minutes" : "30m",
        "1 Hour" : "1h",
        "90 Minutes" : "90m",
        "1 Day" : "1d",
        "5 Days" : "5d",
        "1 Week" : "1wk",
        "1 Month" : "1mo",
        "3 Months" : "3mo"
    }

    # Input fields for backtest parameters
    symbol = st.text_input("Ticker Symbol", placeholder="e.g., AAPL")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    amount = st.number_input("Investment Amount", min_value=0.0, value=1000.0)
    interval = st.selectbox("Data Interval", list(intervals.keys()))

    # Fetch available strategies
    st.sidebar.title("Available Strategies")
    strategies = fetch_strategies()

    if strategies:
        # Strategy selection
        strategy_values = list(strategies.keys())
        selected_strategy = st.sidebar.selectbox("Select Strategy", strategy_values)
      
        # Fetch and display strategy parameters
        st.sidebar.header("Parameter Settings")
        params = fetch_parameters(selected_strategy)
        param_values = {}

        if params:
            # Assuming params is a list of lists [[name, default, min, max], ...]
            for param in params:
                # Unpack the list [name, default, min, max]
                if isinstance(param, list) and len(param) == 4:
                    param_name, default, min_value, max_value = param

                    # Add a checkbox to toggle adjustment
                    adjust = st.sidebar.checkbox(f"Adjust {param_name}", value=False)

                    # Display slider only if checkbox is checked
                    if adjust:
                        param_values[param_name] = st.sidebar.slider(
                            param_name,
                            min_value=min_value,
                            max_value=max_value,
                            value=default
                        )
                    else:
                        # Use the default value if the checkbox is not checked
                        param_values[param_name] = default
                else:
                    st.sidebar.warning(f"Parameter {param} is not in the expected format.")
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
                params_assets = {
                    "ticker_symbol": symbol,
                    "start_date": start_date_str,
                    "end_date": end_date_str,
                    "amount": amount,
                    "time_delta": intervals[interval],
                }

                paramets = {}
                paramets["strategy_params"] = {
                    "name": selected_strategy,
                    "optional_params": param_values
                } 
                paramets["asset_params"] = params_assets
                print("paramets==>",paramets)
                # Call validation endpoint before running backtest
                with st.spinner("Validating parameters..."):
                    validation_response = validate_params(paramets)

                # Handle validation response
                if validation_response:
                    validation_data = validation_response.json()["data"]
                    if validation_data.get("errors"):
                        st.error("Validation Errors:")
                        for error in validation_data["errors"]:
                            st.write(f"- {error}")
                        st.info("Please adjust your inputs and try again.")
                    else:
                        # If validation passes, proceed with backtest
                        with st.spinner("Running backtest..."):
                            response = run_backtest(paramets)

                        # Handle backtest response
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

