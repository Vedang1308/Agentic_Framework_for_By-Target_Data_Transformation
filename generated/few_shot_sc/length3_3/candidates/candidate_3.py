import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms source time-series data into a wide format with hourly aggregations per day.
    
    Source:
        - date: object (format '%m/%d/%Y %H:%M')
        - zone_016: float64
    
    Target:
        - date: object (format '%m/%d/%Y')
        - Hour 1 .. Hour 24: float64
    """
    df = source.copy()
    
    # 1. Parse the datetime column
    # The source date format is '%m/%d/%Y %H:%M'
    df['dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Create the target date string format '%m/%d/%Y'
    df['date_target'] = df['dt'].dt.strftime('%m/%d/%Y')
    
    # 3. Determine the hour bucket for pivoting
    # Hour 0 (00:00-00:59) maps to 'Hour 24'
    # Hour 1 (01:00-01:59) maps to 'Hour 1'
    # ...
    # Hour 23 (23:00-23:59) maps to 'Hour 23'
    df['hour_label'] = df['dt'].dt.hour.apply(lambda h: 'Hour 24' if h == 0 else f'Hour {h}')
    
    # 4. Pivot the table
    # Group by date_target, spread by hour_label, aggregate zone_016
    # Using 'mean' to handle multiple entries per hour (e.g., minutes)
    pivot_df = df.pivot_table(
        index='date_target', 
        columns='hour_label', 
        values='zone_016', 
        aggfunc='mean'
    )
    
    # 5. Reset index to make date a column
    pivot_df = pivot_df.reset_index()
    
    # 6. Rename the index column to 'date' to match target schema
    pivot_df = pivot_df.rename(columns={'date_target': 'date'})
    
    # 7. Ensure all 24 hour columns exist and are in the correct order
    target_hour_cols = [f'Hour {i}' for i in range(1, 25)]
    
    # Reindex columns to ensure all target columns are present, filling missing with NaN
    # First, ensure the 'date' column is first
    cols = ['date'] + target_hour_cols
    
    # Select only the columns that exist in the target schema
    # If any hour column is missing from the pivot (no data for that hour), it won't be in pivot_df.columns
    # We need to add them back as NaN if they are missing
    for col in cols:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # 8. Select and order the final columns
    pivot_df = pivot_df[cols]
    
    return pivot_df