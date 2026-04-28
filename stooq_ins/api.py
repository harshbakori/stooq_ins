import frappe
import requests
import pandas as pd
from io import StringIO

# Get a logger instance for your app
logger = frappe.logger("metal_sync")

@frappe.whitelist()
def sync_metal_prices():
    """Fetch prices for all tickers defined in the 'Metal Ticker' DocType"""
    
    active_metals = frappe.get_all("Metal Ticker", fields=["name", "ticker_symbol"],filters={"enabled": 1})
    
    if not active_metals:
        msg = "No tickers found in Metal Ticker list. Please add records to 'Metal Ticker' first."
        frappe.log_error(msg, "Metal Price Sync Error")
        return msg

    success_count = 0
    error_count = 0

    for metal in active_metals:
        ticker = metal.ticker_symbol
        url = f"https://stooq.com/q/l/?s={ticker.lower()}&f=sd2t2ohlcv&h&e=csv"
        
        try:
            # Debug log for URL being called
            logger.info(f"Syncing {ticker}: Requesting {url}")
            
            response = requests.get(url, timeout=15)
            response.raise_for_status() # Raise error for bad status codes
            
            df = pd.read_csv(StringIO(response.text))
            
            if df.empty or 'Close' not in df.columns:
                logger.warning(f"Syncing {ticker}: Stooq returned empty CSV or missing columns.")
                continue
                
            if str(df['Close'].iloc[0]).upper() == 'N/D':
                logger.warning(f"Syncing {ticker}: Stooq returned N/D (No Data).")
                continue
            
            row = df.iloc[0]
            p_date = row['Date']
            close_val = float(row['Close'])
            
            # Log the data we extracted
            logger.info(f"Syncing {ticker}: Extracted Date {p_date}, Price {close_val}")

            # naming check: Ticker-Date
            doc_name = f"{ticker}-{p_date}"
            
            if not frappe.db.exists("Metal Price", doc_name):
                new_price = frappe.get_doc({
                    "doctype": "Metal Price",
                    "ticker": ticker,
                    "metal_ticker": metal.name, # Link field to Metal Ticker
                    "price_date": p_date,
                    "close_price": close_val,
                    "volume": int(row['Volume']) if pd.notnull(row['Volume']) else 0
                })
                new_price.insert(ignore_permissions=True)
                frappe.db.commit(ignore_permissions=True)
                success_count += 1
                logger.info(f"Syncing {ticker}: Successfully created {doc_name}")
            else:
                logger.info(f"Syncing {ticker}: Record {doc_name} already exists. Skipping.")
                
        except requests.exceptions.RequestException as e:
            error_count += 1
            frappe.log_error(f"Network error for {ticker}: {str(e)}", "Metal Price Sync Error")
        except Exception as e:
            error_count += 1
            frappe.log_error(f"Logic error for {ticker}: {frappe.get_traceback()}", "Metal Price Sync Error")

    return f"Sync Complete. Success: {success_count}, Errors: {error_count}"