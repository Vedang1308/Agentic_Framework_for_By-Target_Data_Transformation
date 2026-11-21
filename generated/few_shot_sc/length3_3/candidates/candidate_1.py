import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse datetime
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string in target format
    df['date_out'] = df['dt'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour and map to target hour index
    # Source hour 0 (0:00-0:59) maps to Target Hour 24
    # Source hour 1 (1:00-1:59) maps to Target Hour 1
    # ...
    # Source hour 23 (23:00-23:59) maps to Target Hour 23
    df['hour_raw'] = df['dt'].dt.hour
    df['hour_target'] = df['hour_raw'].apply(lambda h: 24 if h == 0 else h)
    
    # 4. Group by date and target hour, aggregate zone_016
    # Using mean to handle multiple minutes per hour. 
    # If data is constant, mean equals the value.
    grouped = df.groupby(['date_out', 'hour_target'])['zone_016'].mean()
    
    # 5. Pivot to wide format
    pivot_df = grouped.unstack(fill_value=np.nan)
    
    # 6. Rename columns to 'Hour X'
    pivot_df.columns = [f'Hour {c}' for c in pivot_df.columns]
    
    # 7. Ensure all target columns exist and are in correct order
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # Reset index to make 'date_out' a column
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'date_out': 'date'})
    
    # Select and order columns
    # Note: unstack might not have all 24 columns if they are missing globally.
    # We reindex to ensure all columns are present, filling missing ones with NaN.
    pivot_df = pivot_df.reindex(columns=target_columns)
    
    return pivot_df