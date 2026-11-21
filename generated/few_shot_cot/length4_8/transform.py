import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the datetime column
    # Source format: '7/28/2019 4:50' -> %m/%d/%Y %H:%M
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour for grouping
    df['date_only'] = df['datetime'].dt.date
    df['hour_24'] = df['datetime'].dt.hour
    
    # 3. Define mapping from 24-hour hour to target column names
    # 0 -> 12:00 AM, 1 -> 1:00 AM, ..., 11 -> 11:00 AM
    # 12 -> 12:00 PM, 13 -> 1:00 PM, ..., 23 -> 11:00 PM
    hour_map = {}
    for h in range(24):
        if h == 0:
            label = '12:00 AM'
        elif h < 12:
            label = f'{h}:00 AM'
        elif h == 12:
            label = '12:00 PM'
        else:
            label = f'{h-12}:00 PM'
        hour_map[h] = label
        
    df['hour_label'] = df['hour_24'].map(hour_map)
    
    # 4. Aggregate by date and hour
    # Calculate mean of cerc_logger_1 for each date and hour
    agg_df = df.groupby(['date_only', 'hour_label'])['cerc_logger_1'].mean().reset_index()
    
    # 5. Pivot the data
    # Index: date_only, Columns: hour_label, Values: cerc_logger_1
    pivot_df = agg_df.pivot(index='date_only', columns='hour_label', values='cerc_logger_1')
    
    # 6. Format the date column
    pivot_df.index = pivot_df.index.strftime('%m/%d/%Y')
    pivot_df = pivot_df.reset_index()
    pivot_df.rename(columns={'index': 'date'}, inplace=True)
    
    # 7. Ensure all target columns exist and are in the correct order
    target_columns = [
        'date', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # Fill any missing hours with NaN (or 0 if preferred, but NaN is standard for missing data)
    # The problem statement implies complete data, but robustness is good.
    for col in target_columns[1:]:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # Select and order columns
    result_df = pivot_df[target_columns]
    
    return result_df