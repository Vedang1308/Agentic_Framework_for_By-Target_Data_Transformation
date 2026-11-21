import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # Parse the date column
    df['dt'] = pd.to_datetime(df['date'])
    
    # Extract Date string for grouping/target column
    df['Date'] = df['dt'].dt.strftime('%m/%d/%Y')
    
    # Extract Hour and map to target column names
    # Hour 0 -> Hr 24, Hour 1-23 -> Hr 1-23
    df['HourLabel'] = df['dt'].dt.hour.map(lambda h: 'Hr 24' if h == 0 else f'Hr {h}')
    
    # Aggregate by Date and HourLabel. Using mean as the aggregation function.
    # The source has multiple entries per hour (e.g., every 10 mins).
    aggregated = df.groupby(['Date', 'HourLabel'])['cerc_logger_1'].mean()
    
    # Pivot to wide format
    df_pivot = aggregated.unstack(fill_value=np.nan)
    
    # Reset index to make Date a column
    df_pivot = df_pivot.reset_index()
    
    # Define the expected target columns
    target_hour_cols = [f'Hr {i}' for i in range(1, 25)]
    target_columns = ['Date'] + target_hour_cols
    
    # Ensure all hour columns exist, even if some dates have missing data
    for col in target_hour_cols:
        if col not in df_pivot.columns:
            df_pivot[col] = np.nan
            
    # Select and order columns verbatim
    df_result = df_pivot[target_columns]
    
    # Sort by Date to match typical output expectations, though not strictly required by schema
    # The target sample is not sorted chronologically, but usually deterministic output is preferred.
    # However, to be safe and general, we will just return the grouped result. 
    # If strict ordering is needed, one might sort by Date. 
    # Given the target sample order (05/08, 05/07, 03/10...), it's not sorted. 
    # We will leave the order as determined by groupby (which is usually sorted by key).
    
    return df_result