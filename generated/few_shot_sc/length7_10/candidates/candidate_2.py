import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms source DataFrame with 'date' and 'cerc_logger_1' into a target DataFrame
    with 'month', 'daytype', and 'hr1'...'hr24' columns.
    """
    df = source.copy()
    
    # 1. Parse the date column
    # Format: '%m/%d/%Y %H:%M'
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Month Name
    df['month'] = df['datetime'].dt.strftime('%B')
    
    # 3. Determine Day Type (weekday vs weekend)
    # dayofweek: 0=Monday, ..., 4=Friday, 5=Saturday, 6=Sunday
    df['daytype'] = np.where(df['datetime'].dt.dayofweek < 5, 'weekday', 'weekend')
    
    # 4. Extract Hour and map to target column names
    # Hour 0 (00:00-00:59) -> 'hr1'
    # Hour 1 (01:00-01:59) -> 'hr2'
    # ...
    # Hour 23 (23:00-23:59) -> 'hr24'
    df['hour'] = df['datetime'].dt.hour
    df['hr_col'] = 'hr' + (df['hour'] + 1).astype(str)
    
    # 5. Aggregate: Mean of cerc_logger_1 for each month, daytype, and hour column
    # Using pivot_table for clarity
    pivot_df = df.pivot_table(
        index=['month', 'daytype'],
        columns='hr_col',
        values='cerc_logger_1',
        aggfunc='mean'
    )
    
    # 6. Ensure all 24 hour columns exist and are in correct order
    target_hour_cols = [f'hr{i}' for i in range(1, 25)]
    
    # Reindex columns to ensure all hr1..hr24 are present, filling missing with NaN
    pivot_df = pivot_df.reindex(columns=target_hour_cols)
    
    # 7. Reset index to make month and daytype columns again
    result_df = pivot_df.reset_index()
    
    # 8. Select and order the final columns
    target_columns = ['month', 'daytype'] + target_hour_cols
    
    return result_df[target_columns]