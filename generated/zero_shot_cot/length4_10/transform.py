import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame from long format (timestamp, value) 
    to wide format (date, hourly values in 12-hour format).
    """
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract calendar date and hour
    df['date_only'] = df['datetime'].dt.strftime('%m/%d/%Y')
    df['hour_24'] = df['datetime'].dt.hour
    
    # 3. Map 24-hour format to 12-hour AM/PM format strings
    def map_hour_to_label(h):
        if h == 0:
            return '12:00 AM'
        elif h < 12:
            return f'{h}:00 AM'
        elif h == 12:
            return '12:00 PM'
        else:
            return f'{h-12}:00 PM'
    
    df['hour_label'] = df['hour_24'].apply(map_hour_to_label)
    
    # 4. Aggregate and Pivot
    # We group by date and hour_label, then take the mean of the cooling setpoint.
    # Using mean handles the multiple 5-minute intervals per hour.
    pivot_df = df.groupby(['date_only', 'hour_label'])['zone_016_cooling_sp'].mean().reset_index()
    
    # Pivot to wide format
    wide_df = pivot_df.pivot(index='date_only', columns='hour_label', values='zone_016_cooling_sp')
    
    # Reset index to make date a column
    wide_df = wide_df.reset_index()
    wide_df.rename(columns={'index': 'date'}, inplace=True)
    
    # 5. Define the exact target column order
    target_columns = [
        'date', 
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', 
        '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', 
        '12:00 AM'
    ]
    
    # Ensure all target columns exist, filling missing ones with NaN if necessary
    for col in target_columns:
        if col not in wide_df.columns:
            wide_df[col] = np.nan
            
    # Select and order columns
    result_df = wide_df[target_columns]
    
    return result_df