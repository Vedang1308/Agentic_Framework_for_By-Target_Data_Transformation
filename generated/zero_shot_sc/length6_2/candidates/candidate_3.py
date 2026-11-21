import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by:
    1. Parsing the 'CST' date column to extract the date in 'MM/DD/YYYY' format.
    2. Renaming the hourly columns from 'H:00'/'24:00:00' format to 'Hr H' format.
    3. Reordering columns to match the target schema.
    """
    df = source.copy()
    
    # 1. Transform the Date column
    # Source format: 'Sat 12/01/2012'
    # Target format: '12/01/2012'
    # We can remove the first 4 characters (Day name + space)
    df['Date'] = df['CST'].str.replace(r'^\w{3}\s', '', regex=True)
    
    # 2. Rename the hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'Hr 1', 'Hr 2', ..., 'Hr 23', 'Hr 24'
    
    rename_map = {}
    for col in df.columns:
        if col == 'CST':
            continue # Skip the date column, we already created 'Date'
        
        # Check if the column is an hour column
        # It should start with a digit
        if col[0].isdigit():
            # Extract the hour number. 
            # Examples: '1:00' -> 1, '24:00:00' -> 24
            # Split by ':' and take the first part
            hour_str = col.split(':')[0]
            hour_num = int(hour_str)
            rename_map[col] = f'Hr {hour_num}'
            
    df.rename(columns=rename_map, inplace=True)
    
    # 3. Define the target column order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 4. Select and reorder columns to match target schema exactly
    # Ensure all target columns exist
    df = df[target_columns]
    
    return df[target_columns]