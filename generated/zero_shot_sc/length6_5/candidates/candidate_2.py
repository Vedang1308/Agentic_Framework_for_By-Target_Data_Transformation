import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by:
    1. Dropping the 'Class' column.
    2. Renaming hourly columns from integers (1-24) to 'Hr 1'-'Hr 24'.
    3. Formatting the 'Date' column to '%m/%d/%Y' (ensuring zero-padding).
    4. Sorting by Date.
    5. Returning the DataFrame with exact target column names.
    """
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Define target columns
    target_columns = [
        'Date', 'Hr 1', 'Hr 2', 'Hr 3', 'Hr 4', 'Hr 5', 'Hr 6', 'Hr 7', 'Hr 8', 
        'Hr 9', 'Hr 10', 'Hr 11', 'Hr 12', 'Hr 13', 'Hr 14', 'Hr 15', 'Hr 16', 
        'Hr 17', 'Hr 18', 'Hr 19', 'Hr 20', 'Hr 21', 'Hr 22', 'Hr 23', 'Hr 24'
    ]
    
    # 1. Drop the 'Class' column as it is not in the target schema
    if 'Class' in df.columns:
        df = df.drop(columns=['Class'])
        
    # 2. Rename the hourly columns
    # Source columns are integers 1 to 24 (based on schema description)
    # Target columns are strings 'Hr 1' to 'Hr 24'
    rename_map = {col: f'Hr {col}' for col in range(1, 25)}
    df = df.rename(columns=rename_map)
    
    # 3. Format the Date column
    # Parse dates to datetime objects to handle formatting consistently
    # The target sample shows zero-padded dates (e.g., 01/01/2013)
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%m/%d/%Y')
    
    # 4. Sort by Date to ensure chronological order
    # Converting back to datetime for sorting, then keeping the string format
    df['Date_dt'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date_dt').drop(columns=['Date_dt']).reset_index(drop=True)
    
    # 5. Ensure column order matches target exactly
    # Filter for only the target columns to ensure no extra columns remain
    df = df[target_columns]
    
    return df[target_columns]