import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the CST column to extract date information
    # Format: '%a %m/%d/%Y' e.g., 'Sat 12/01/2012'
    df['parsed_date'] = pd.to_datetime(df['CST'], format='%a %m/%d/%Y')
    
    # 2. Extract 'month' as full month name (e.g., 'April', 'November')
    df['month'] = df['parsed_date'].dt.strftime('%B')
    
    # 3. Determine 'daytype' based on day of the week
    # 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday, 5=Saturday, 6=Sunday
    # Weekdays: 0-4, Weekends: 5-6
    df['daytype'] = df['parsed_date'].dt.dayofweek.apply(lambda x: 'weekend' if x >= 5 else 'weekday')
    
    # 4. Rename the hour columns
    # Source columns: '1:00', '2:00', ..., '23:00', '24:00:00'
    # Target columns: 'hr1', 'hr2', ..., 'hr23', 'hr24'
    
    col_mapping = {}
    for i in range(1, 24):
        src_col = f'{i}:00'
        tgt_col = f'hr{i}'
        col_mapping[src_col] = tgt_col
        
    # Handle the 24th hour specifically as it has a different format '24:00:00'
    col_mapping['24:00:00'] = 'hr24'
    
    df = df.rename(columns=col_mapping)
    
    # 5. Define the target columns in the correct order
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # 6. Select only the required columns
    # Ensure all columns exist to avoid errors
    existing_cols = [col for col in target_columns if col in df.columns]
    df = df[existing_cols]
    
    # 7. Return the DataFrame with exact target column names
    return df[target_columns]