import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame (long format, minute-level data) 
    into the target DataFrame (wide format, hourly aggregates per day).
    
    Mapping Logic:
    - Source hour 0 (00:00-01:00) maps to 'Hour 24'
    - Source hour 1 (01:00-02:00) maps to 'Hour 1'
    - ...
    - Source hour 23 (23:00-24:00) maps to 'Hour 23'
    """
    
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour components
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map hours to target column labels
    # Hour 0 -> 'Hour 24'
    # Hour 1-23 -> 'Hour 1' - 'Hour 23'
    def get_hour_label(h):
        if h == 0:
            return 'Hour 24'
        else:
            return f'Hour {h}'
            
    df['hour_label'] = df['hour'].apply(get_hour_label)
    
    # 4. Aggregate by date and hour_label
    # Using mean to handle multiple minutes per hour
    pivot_df = df.groupby(['date_only', 'hour_label'])['zone_016'].mean().reset_index()
    
    # 5. Pivot to wide format
    wide_df = pivot_df.pivot(index='date_only', columns='hour_label', values='zone_016')
    
    # 6. Ensure all hour columns exist and are in the correct order
    # Define the expected column names
    hour_columns = [f'Hour {i}' for i in range(1, 24)] + ['Hour 24']
    
    # Reindex columns to ensure all are present (missing ones become NaN)
    wide_df = wide_df.reindex(columns=hour_columns)
    
    # 7. Reset index and rename date column
    wide_df = wide_df.reset_index()
    wide_df = wide_df.rename(columns={'date_only': 'date'})
    
    # 8. Format the date column to '%m/%d/%Y'
    wide_df['date'] = pd.to_datetime(wide_df['date']).dt.strftime('%m/%d/%Y')
    
    # 9. Define final target columns
    target_columns = ['date'] + hour_columns
    
    # 10. Return the dataframe with exact column names
    return wide_df[target_columns]