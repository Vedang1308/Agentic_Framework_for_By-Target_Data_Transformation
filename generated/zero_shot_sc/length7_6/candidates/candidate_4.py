import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame containing daily hourly load profiles
    into a target DataFrame with month, daytype, and renamed hourly columns.
    """
    df = source.copy()
    
    # 1. Parse the Date column
    # The format is '%m/%d/%Y' e.g., '7/3/2013'
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Extract Month Name
    # %B gives full month name (e.g., July, January)
    df['month'] = df['parsed_date'].dt.strftime('%B')
    
    # 3. Determine Day Type
    # Weekday (Mon-Fri) vs Weekend (Sat-Sun)
    # dayofweek: 0=Monday, ..., 4=Friday, 5=Saturday, 6=Sunday
    df['daytype'] = np.where(df['parsed_date'].dt.dayofweek < 5, 'weekday', 'weekend')
    
    # 4. Rename Hourly Columns
    # Source columns are '1', '2', ..., '24' (strings)
    # Target columns are 'hr1', 'hr2', ..., 'hr24'
    rename_map = {str(i): f'hr{i}' for i in range(1, 25)}
    df = df.rename(columns=rename_map)
    
    # 5. Select and Order Columns
    # Target columns: month, daytype, hr1 ... hr24
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # Ensure numeric columns are float
    for col in [f'hr{i}' for i in range(1, 25)]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # 6. Return the transformed DataFrame
    return df[target_columns]