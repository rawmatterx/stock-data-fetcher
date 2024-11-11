import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
import logging
from io import StringIO
import base64
import requests
import json
import yfinance as yf

# Setup logging
logging.basicConfig(level=logging.INFO)

def get_stock_data(symbol, start_date, end_date, retries=3):
    """
    Fetch stock data with enhanced retry mechanism and error handling
    """
    for attempt in range(retries):
        try:
            # Add a delay between attempts
            if attempt > 0:
                time.sleep(2 * attempt)  # Increasing delay for each retry

            # Create Ticker object
            ticker = yf.Ticker(f"{symbol}.NS")
            
            # Fetch data
            df = ticker.history(
                start=start_date,
                end=end_date,
                interval="1d"
            )
            
            if not df.empty:
                df['Symbol'] = symbol
                df = df.reset_index()
                st.write(f"✅ Successfully fetched data for {symbol}")
                return df
            else:
                st.warning(f"⚠️ Empty data received for {symbol}")
                return None

        except Exception as e:
            st.warning(f"⚠️ Attempt {attempt + 1} failed for {symbol}: {str(e)}")
            if attempt == retries - 1:
                st.error(f"❌ Failed to fetch data for {symbol} after {retries} attempts: {str(e)}")
                return None

def get_download_link(df, filename="stock_data.csv"):
    """Generate a download link for the dataframe"""
    try:
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" class="download-button">Download CSV file</a>'
        return href
    except Exception as e:
        st.error(f"Error generating download link: {str(e)}")
        return None

def main():
    # Page config
    st.set_page_config(
        page_title="Stock Data Fetcher",
        page_icon="📈",
        layout="wide"
    )

    # Custom CSS
    st.markdown("""
        <style>
        .download-button {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("📈 Stock Data Fetcher")
    st.markdown("""
    ### Instructions:
    1. Upload a text file containing stock symbols (one per line)
    2. Select your desired date range
    3. Click 'Fetch Data'
    
    **Note:** Please ensure your stock symbols are correct NSE codes.
    """)

    uploaded_file = st.file_uploader("Choose a .txt file with stock symbols", type="txt")

    if uploaded_file is not None:
        try:
            # Read and display the symbols
            string_data = StringIO(uploaded_file.getvalue().decode("utf-8"))
            symbols = [line.strip() for line in string_data.readlines() if line.strip()]
            
            st.write("📋 Loaded symbols:", ", ".join(symbols))

            # Date range selection
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input(
                    "Start date",
                    datetime.now() - timedelta(days=365)
                )
            with col2:
                end_date = st.date_input(
                    "End date",
                    datetime.now()
                )

            if st.button("🚀 Fetch Data"):
                if start_date >= end_date:
                    st.error("❌ Start date must be before end date")
                    return

                # Initialize progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                all_data = []
                failed_symbols = []

                # Fetch data with progress tracking
                for i, symbol in enumerate(symbols):
                    status_text.text(f"⏳ Processing {symbol}...")
                    df = get_stock_data(symbol, start_date, end_date)
                    
                    if df is not None:
                        all_data.append(df)
                    else:
                        failed_symbols.append(symbol)
                    
                    # Update progress
                    progress = (i + 1) / len(symbols)
                    progress_bar.progress(progress)
                    
                    # Add delay to avoid rate limiting
                    time.sleep(1.5)

                if all_data:
                    # Combine all data
                    combined_df = pd.concat(all_data, ignore_index=True)
                    
                    # Display summary
                    st.success(f"✅ Successfully fetched data for {len(all_data)} stocks")
                    
                    if failed_symbols:
                        st.warning(f"⚠️ Failed to fetch data for {len(failed_symbols)} symbols: {', '.join(failed_symbols)}")

                    # Display preview
                    st.write("📊 Preview of the data:")
                    st.dataframe(combined_df.head())

                    # Generate download link
                    output_filename = f'stock_data_{start_date.strftime("%Y%m%d")}_{end_date.strftime("%Y%m%d")}.csv'
                    download_link = get_download_link(combined_df, output_filename)
                    if download_link:
                        st.markdown(download_link, unsafe_allow_html=True)
                else:
                    st.error("❌ No data was collected. Please check the symbols and try again.")

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            logging.exception("Error in main function")

    # Footer
    st.markdown("---")
    st.markdown("📈 Made for NSE stocks data fetching")

if __name__ == "__main__":
    main()