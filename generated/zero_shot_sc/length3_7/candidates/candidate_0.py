import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with columns ['Date', 'Class', 1..24]
    into a target DataFrame with columns ['date', 'Hour 1'..'Hour 24'].
    
    Steps:
    1. Rename 'Date' to 'date'.
    2. Format 'date' to %m/%d/%Y (ensuring zero-padding).
    3. Rename numeric columns 1-24 to 'Hour 1'-'Hour 24'.
    4. Drop the 'Class' column.
    5. Sort by date.
    6. Return the dataframe with target columns.
    """
    df = source.copy()
    
    # 1. Rename the Date column
    df.rename(columns={'Date': 'date'}, inplace=True)
    
    # 2. Format the date column to ensure consistent %m/%d/%Y format
    # Parse as datetime to handle any irregularities, then format back to string
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y').dt.strftime('%m/%d/%Y')
    
    # 3. Rename numeric columns 1-24 to 'Hour 1'-'Hour 24'
    # Create a mapping for columns 1 through 24
    hour_mapping = {i: f'Hour {i}' for i in range(1, 25)}
    df.rename(columns=hour_mapping, inplace=True)
    
    # 4. Drop the 'Class' column as it is not in the target schema
    if 'Class' in df.columns:
        df.drop(columns=['Class'], inplace=True)
    
    # 5. Define the target columns in the required order
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 6. Sort by date to ensure deterministic order (optional but good practice)
    # Since date is string %m/%d/%Y, sorting alphabetically works correctly for this format
    df.sort_values(by='date', inplace=True)
    
    # 7. Reset index to clean up
    df.reset_index(drop=True, inplace=True)
    
    # 8. Return only the target columns
    return df[target_columns]