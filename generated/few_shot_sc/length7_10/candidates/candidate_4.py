import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms source time-series data into a monthly/hourly average profile
    grouped by day type (weekday/weekend).
    """
    df = source.copy()
    
    # 1. Parse datetime
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract features
    df['month'] = df['datetime'].dt.strftime('%B') # e.g., 'August'
    df['hour'] = df['datetime'].dt.hour # 0-23
    
    # Determine day type: 0-4 (Mon-Fri) -> weekday, 5-6 (Sat-Sun) -> weekend
    df['daytype'] = np.where(df['datetime'].dt.weekday >= 5, 'weekend', 'weekday')
    
    # 3. Aggregate by month, daytype, and hour
    # We take the mean of the sensor readings for each hour slot
    grouped = df.groupby(['month', 'daytype', 'hour'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot the table
    # Rows: month, daytype
    # Columns: hour (0-23)
    # Values: mean cerc_logger_1
    pivot_df = grouped.pivot_table(index=['month', 'daytype'], columns='hour', values='cerc_logger_1')
    
    # 5. Rename columns to hr1...hr24
    # Source hour 0 corresponds to hr1 (12am-1am)
    # Source hour 23 corresponds to hr24 (11pm-12am)
    new_columns = {h: f'hr{h+1}' for h in range(24)}
    pivot_df = pivot_df.rename(columns=new_columns)
    
    # 6. Reset index to get month and daytype back as columns
    result_df = pivot_df.reset_index()
    
    # 7. Define target columns
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]
    
    # Ensure all columns exist (in case some hours are missing, though unlikely with full data)
    for col in target_columns:
        if col not in result_df.columns:
            result_df[col] = np.nan
            
    # 8. Return with exact column order
    return result_df[target_columns]