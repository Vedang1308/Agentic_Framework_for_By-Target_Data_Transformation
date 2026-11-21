import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame format.
    
    Steps:
    1. Rename the 'CST' column to 'Date' and format the date string.
    2. Rename the hourly columns (1:00, ..., 24:00:00) to (Hr 1, ..., Hr 24).
    3. Ensure the column order matches the target schema.
    """
    # Create a copy to avoid modifying the original source
    df = source.copy()
    
    # 1. Process the Date column
    # Source format: '%a %m/%d/%Y' (e.g., 'Sat 12/01/2012')
    # Target format: '%m/%d/%Y' (e.g., '12/01/2012')
    # We can extract the date part by splitting or using datetime parsing.
    # Since the day name is always 3 chars + space, we can slice or split.
    # Using pd.to_datetime is robust.
    df['Date'] = pd.to_datetime(df['CST'], format='%a %m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # 2. Rename the hourly columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'Hr 1', 'Hr 2', ..., 'Hr 23', 'Hr 24'
    
    # Define the mapping for all 24 hours
    rename_mapping = {}
    
    # Hours 1 to 23
    for h in range(1, 24):
        src_col = f"{h}:00"
        tgt_col = f"Hr {h}"
        rename_mapping[src_col] = tgt_col
        
    # Hour 24 (special format in source: '24:00:00')
    rename_mapping['24:00:00'] = 'Hr 24'
    
    # Apply the renaming
    df = df.rename(columns=rename_mapping)
    
    # 3. Select and order the columns according to the target schema
    target_columns = [
        'Date', 'Hr 1', 'Hr 2', 'Hr 3', 'Hr 4', 'Hr 5', 'Hr 6', 'Hr 7', 
        'Hr 8', 'Hr 9', 'Hr 10', 'Hr 11', 'Hr 12', 'Hr 13', 'Hr 14', 'Hr 15', 
        'Hr 16', 'Hr 17', 'Hr 18', 'Hr 19', 'Hr 20', 'Hr 21', 'Hr 22', 'Hr 23', 'Hr 24'
    ]
    
    # Ensure we only return the required columns in the correct order
    # Drop the original 'CST' column if it still exists (it should be replaced by 'Date' logic, but let's be safe)
    if 'CST' in df.columns:
        df = df.drop(columns=['CST'])
        
    # Return the dataframe with the exact target columns
    return df[target_columns]