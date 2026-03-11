import os
import logging
import pandas as pd


# Ensure logs directory exists
os.makedirs("logs" , exist_ok=True)


# Configure Logging 
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

logging.info("Logging Initialized.")


def load_data(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
        logging.info(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        logging.info(f"Columns: {list(df.columns)}")
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {path}")
        raise
    except Exception as e:
        logging.error(f"Error loading dataset: {e}")
        raise

def check_nulls(df : pd.DataFrame) -> None:
    null_cols = df.isnull().sum()
    null_cols = null_cols[null_cols > 0]

    if not null_cols.empty:
        logging.warning(f"Columns with nulls: \n{null_cols}")
    else:
        logging.info("No Nulls Found.")


def total_revenue(df: pd.DataFrame) -> pd.DataFrame:
    if 'discounted_price' in df.columns:
        df['total_revenue'] = df['discounted_price'] * 1 # assume quantity as 1 if missing
        total = df['total_revenue'].sum()

        logging.info(f"Total Revenue : {total}")
    else:
        logging.warning("Column 'discounted_price' not Found.")

    return df

def main():
    logging.info("Sales Pipeline Started.")

    data_path = os.path.join(os.getcwd() , "data" , "raw" , "amazon.csv")

    df = load_data(data_path)

    check_nulls(df)
    
    df = total_revenue(df)

   
    


# Only run main if this file is executed directly
if __name__ == "__main__":
    main()