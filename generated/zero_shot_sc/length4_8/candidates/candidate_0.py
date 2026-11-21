import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    # Source format: '7/28/2019 4:50' -> %m/%d/%Y %I:%M (note: source uses 24h or 12h? 
    # Sample '4:50' could be 4:50 AM or PM. '23:30' is clearly 24h. 
    # So source is %m/%d/%Y %H:%M
    
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date string for grouping and final output
    # Target format: '05/08/2019' -> %m/%d/%Y
    df['date_str'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour and map to target column names
    # 0 -> 12:00 AM, 1 -> 1:00 AM, ..., 11 -> 11:00 AM, 12 -> 12:00 PM, ..., 23 -> 11:00 PM
    hour = df['datetime'].dt.hour
    
    def map_hour_to_label(h):
        if h == 0:
            return '12:00 AM'
        elif 1 <= h <= 11:
            return f'{h}:00 AM'
        elif h == 12:
            return '12:00 PM'
        else: # 13-23
            return f'{h-12}:00 PM'
            
    df['hour_label'] = hour.map(map_hour_to_label)
    
    # 4. Aggregate by date and hour
    # We assume the target values are the mean of the readings in that hour
    agg_df = df.groupby(['date_str', 'hour_label'])['cerc_logger_1'].mean().reset_index()
    
    # 5. Pivot to wide format
    # Rows: date_str, Columns: hour_label, Values: cerc_logger_1
    pivot_df = agg_df.pivot_table(index='date_str', columns='hour_label', values='cerc_logger_1')
    
    # 6. Define target columns in the exact required order
    target_columns = [
        'date', 
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', 
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    # 7. Reindex columns to ensure all target hours are present and in correct order
    # If some hours are missing in the data, they will be NaN. 
    # The problem statement implies a dense dataset, but we should handle missing cols gracefully.
    hour_cols = target_columns[1:] # Exclude 'date'
    pivot_df = pivot_df.reindex(columns=hour_cols)
    
    # 8. Reset index to make date a column and rename it
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'date_str': 'date'})
    
    # 9. Select and order columns to match target exactly
    # Note: reindex might have introduced NaNs if data is missing, but we return the structure.
    result_df = pivot_df[target_columns]
    
    return result_df